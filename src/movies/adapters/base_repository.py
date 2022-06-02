from typing import List, Optional
from abc import ABC, abstractmethod

from movies.utils.movie_fetcher import get_movies
from movies.domain.movie_model import Movie
from movies.domain.user_model import User

class BaseRepository(ABC):
    @abstractmethod
    def get_user(self, username: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def store_user(self, username: str, email: str, preferences: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def clean_movies(self):
        raise NotImplementedError

    @abstractmethod
    def get_movies(self, preference_key: int, descending: bool) -> List[Movie]:
        raise NotImplementedError

    @abstractmethod
    def store_movie(self, movie_id: int, preference_key: int, movie_title: str, rating: float, year: int) -> None:
        raise NotImplementedError

    def re_populate_movies(self):
        movies = get_movies()
        self.clean_movies()
        for movie in movies:
            self.store_movie(**movie)

    @abstractmethod
    def drop_all(self):
        raise NotImplementedError
