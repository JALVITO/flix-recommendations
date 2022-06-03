import pytest

from src.movies.recommendations.category_product import CategoryProduct
from src.movies.domain.category import Category

@pytest.fixture
def category_product():
    return CategoryProduct()

testdata = [
    # (1 * 2 * 5) % 5 + 1 = 10 % 5 + 1 = 1
    ([Category.COMEDY, Category.DRAMA, Category.ADVENTURE], 1),
    # (1 * 2 * 3) % 5 + 1 = 6 % 5 + 1 = 2
    ([Category.COMEDY, Category.DRAMA, Category.SCI_FI], 2),
    # (1 * 3 * 4) % 5 + 1 = 12 % 5 + 1 = 3
    ([Category.COMEDY, Category.SCI_FI, Category.ROMANTIC], 3),
    # (1 * 2 * 4) % 5 + 1 = 8 % 5 + 1 = 4
    ([Category.COMEDY, Category.DRAMA, Category.ROMANTIC], 4),
    # (2 * 3 * 4) % 5 + 1 = 24 % 5 + 1 = 5
    ([Category.DRAMA, Category.SCI_FI, Category.ROMANTIC], 5),
]

@pytest.mark.parametrize('categories,expected_key', testdata, ids=[f'key_{data[-1]}' for data in testdata])
def test_category_product_operation(category_product: CategoryProduct, categories: list[Category], expected_key: int):
    assert category_product.generate_preference_key(categories) == expected_key