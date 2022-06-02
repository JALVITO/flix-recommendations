from abc import ABC, abstractmethod

from movies.domain.category import Category

# Design Patterns (2/2): Strategy is being used here, as we define an umbrella for recommendation
# algorithms to use. We can create new strategies by subclassing this abstract class.

# SOLID (2/3): Open-Closed principle is used here. If a new algorithm is designed, it can extend
# with this abstract class without the need to modify existing code.
class RecommendationAlgorithm(ABC):
    @abstractmethod
    def generate_preference_key(self, preferences: list[Category]) -> int:
        raise NotImplementedError
