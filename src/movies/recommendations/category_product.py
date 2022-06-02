import math

from movies.domain.category import Category
from movies.recommendations.recommendation_algorithm import RecommendationAlgorithm

class CategoryProduct(RecommendationAlgorithm):
    def generate_preference_key(self, preferences: list[Category]) -> int:
        return math.prod((pref for pref in preferences)) % len(Category) + 1