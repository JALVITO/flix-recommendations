import os

from contextlib import contextmanager
from typing import Generator, List, Optional

from sqlalchemy import orm
from sqlalchemy.engine import create_engine
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from movies.models.base_model import Base
from movies.models.movie_model import Movie
from movies.models.user_model import User


@contextmanager
def create_scoped_session(
    scoped_session: orm.scoped_session,
    ignore_integrity_error: bool = False,
) -> Generator[Session, None, None]:
    session = scoped_session()
    try:
        yield session
        session.commit()
    except IntegrityError as err:
        session.rollback()
        if ignore_integrity_error:
            print(
                f"Ignoring {repr(err)}. This happens due to a timing issue among threads/processes/"
                "nodes. Another one might have committed a record with the same key(s)."
            )
        else:
            raise
    except SQLAlchemyError as err:
        session.rollback()
        message = (
            "An exception is raised during the commit. "
            "This typically happens due to invalid data in the commit, "
            "e.g. exceeding max length. "
        )
        raise ValueError(message) from err
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def get_postgres_uri():
    host = os.environ.get("DB_HOST", "postgres")
    port = 5432
    password = os.environ.get("DB_PASS", "abc123")
    user, db_name = "movies", "movies"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

class Storage():
    def __init__(self):
        try:
            self.engine = create_engine(get_postgres_uri(),
            isolation_level="REPEATABLE READ",
            )
        except ImportError as err:
            raise ImportError(
                "Failed to import DB access module for the specified storage URL. "
                "Please install appropriate one."
            ) from err
        self.scoped_session = orm.scoped_session(
            orm.sessionmaker(bind=self.engine, expire_on_commit=False)
        )
        Base.metadata.create_all(self.engine)

    def get_user(self, username: str) -> Optional[User]:
        try:
            with create_scoped_session(self.scoped_session) as session:
                return User.find_or_raise_by_name(username, session)
        except KeyError:
            return None

    def store_user(self, username: str, email: str, preferences: str):
        try:
            with create_scoped_session(self.scoped_session) as session:
                return User.add_user(username, email, preferences, session)
        except IntegrityError:
            return None

    def clean_movies(self):
        with create_scoped_session(self.scoped_session) as session:
            Movie.clean_movies(session=session)

    def get_movies(self, preference_key: int, descending: bool) -> List[Movie]:
        with create_scoped_session(self.scoped_session) as session:
            return Movie.find_or_raise_by_preference_key(preference_key, descending, session)

    def store_movie(self, movie_id: int, preference_key: int, movie_title: str, rating: float, year: int):
        with create_scoped_session(self.scoped_session) as session:
            return Movie.add_movie(movie_id, preference_key, movie_title, rating, year, session)
