import requests
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup

from movies.sql_alchemy_config import get_postgres_uri
from movies.category import Category

DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        get_postgres_uri(),
        isolation_level="REPEATABLE READ",
    )
)
session = DEFAULT_SESSION_FACTORY()


def get_movies():
    # Downloading imdb top 250 movie's data
    url = 'http://www.imdb.com/chart/top'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    movies = soup.select('td.titleColumn')
    # links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
    # crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
    ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
    # votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]

    # create a empty list for storing
    # movie information
    arr = []

    # Iterating over movies to extract
    # each movie's details
    for index, tag in enumerate(movies):
        # Separating movie into: 'place',
        # 'title', 'year'
        movie_string = tag.get_text()
        movie = (' '.join(movie_string.split()).replace('.', ''))
        movie_title = movie[len(str(index)) + 1:-7]
        year = re.search(r'\((.*?)\)', movie_string).group(1)

        data = {
            "movie_id": index,
            "preference_key": index % len(Category) + 1,
            "movie_title": movie_title,
            "rating": ratings[index],
            "year": year,
        }
        arr.append(data)

    return arr
