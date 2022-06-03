from sqlalchemy import (
    Column,
    String,
)

from sqlalchemy.orm import Session
from src.movies.domain.base_model import Base

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True)
    email = Column(String)
    preferences = Column(String)

    # SOLID (1/3): Dependency inversion is used here, when the Session is sent to the model class
    # methods, so it does not generate a direct dependency and is instead fed that component.
    @classmethod
    def find_or_raise_by_name(cls, username: str, session: Session):
        query = session.query(cls).filter(cls.username == username)
        user = query.one_or_none()
        return user

    # SOLID (1/3): Dependency inversion is used here, when the Session is sent to the model class
    # methods, so it does not generate a direct dependency and is instead fed that component.
    @classmethod
    def add_user(cls, username: str, email: str, preferences: str, session: Session):
        user = User(username=username, email=email, preferences=preferences)
        session.add(user)
        return user

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

