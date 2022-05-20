from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
)

from sqlalchemy.orm import Session
from movies.models.base_model import Base

class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    preference_key = Column(Integer)
    movie_title = Column(String)
    rating = Column(Float)
    year = Column(Integer)

    # SOLID (1/3): Dependency inversion is used here, when the Session is sent to the model class
    # methods, so it does not generate a direct dependency and is instead fed that component.
    @classmethod
    def find_or_raise_by_preference_key(cls, preference_key: int, descending: bool, session: Session):
        order = cls.rating.desc() if descending else cls.rating
        movies = session.query(cls).filter(cls.preference_key == preference_key).order_by(order).limit(10).all()
        if movies is None:
            raise KeyError('Record does not exist')
        return movies

    # SOLID (1/3): Dependency inversion is used here, when the Session is sent to the model class
    # methods, so it does not generate a direct dependency and is instead fed that component.
    @classmethod
    def add_movie(cls, movie_id: int, preference_key: int, movie_title: str, rating: float, year: int, session: Session):
        movie = Movie(movie_id=movie_id, preference_key=preference_key, movie_title=movie_title, rating=rating, year=year)
        session.add(movie)
        return movie

    # SOLID (1/3): Dependency inversion is used here, when the Session is sent to the model class
    # methods, so it does not generate a direct dependency and is instead fed that component.
    @classmethod
    def clean_movies(cls, session: Session):
        session.query(cls).delete()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in ['preference_key', 'movie_id']}