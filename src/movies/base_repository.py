from typing import List, Optional
from abc import ABC, abstractmethod

from movies.models.movie_model import Movie
from movies.models.user_model import User

class BaseRepository(ABC):
    @abstractmethod
    def get_user(self, username: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def store_user(self, username: str, email: str, preferences: str):
        raise NotImplementedError

    @abstractmethod
    def clean_movies(self):
        raise NotImplementedError

    @abstractmethod
    def get_movies(self, preference_key: int, descending: bool) -> List[Movie]:
        raise NotImplementedError

    @abstractmethod
    def store_movie(self, movie_id: int, preference_key: int, movie_title: str, rating: float, year: int):
        raise NotImplementedError
