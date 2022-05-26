from typing import List, Optional
from abc import ABC, abstractmethod

from movies.models.movie_model import Movie
from movies.models.user_model import User

class BaseRepository(ABC):
    @abstractmethod
    def get_user(self, username: str) -> Optional[User]:
        ...

    @abstractmethod
    def store_user(self, username: str, email: str, preferences: str):
        ...

    @abstractmethod
    def clean_movies(self):
        ...

    @abstractmethod
    def get_movies(self, preference_key: int, descending: bool) -> List[Movie]:
        ...

    @abstractmethod
    def store_movie(self, movie_id: int, preference_key: int, movie_title: str, rating: float, year: int):
        ...
