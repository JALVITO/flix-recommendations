from enum import Enum
from movies.recommendations.category_product import CategoryProduct
from movies.recommendations.recommendation_algorithm import RecommendationAlgorithm

class AlgorithmType(Enum):
    CATEGORY_PRODUCT = 1

# Design Pattern (1/2): This SimpleFactory can create a recommender of any type provided the
# corresponding AlgorithmType enum value.
class RecommenderFactory:
    # SOLID (3/3): Liskov Substitution Principle allows us to return any Recommender algorithm
    # subclass, since it can be substituted without issues in the client code.
    @staticmethod
    def create_recommender(algorithm_type: AlgorithmType) -> RecommendationAlgorithm:
        if (algorithm_type == AlgorithmType.CATEGORY_PRODUCT):
            return CategoryProduct()
        
        raise Exception('Invalid algorithm type')