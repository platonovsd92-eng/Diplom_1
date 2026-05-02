import pytest
from unittest.mock import Mock
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient


@pytest.fixture
def mock_bun():
    """Фикстура: мок булочки"""
    bun_mock = Mock(spec=Bun)
    bun_mock.get_name.return_value = "black bun"
    bun_mock.get_price.return_value = 100
    return bun_mock


@pytest.fixture
def mock_ingredient_sauce():
    """Фикстура: мок ингредиента типа соус"""
    ingredient_mock = Mock(spec=Ingredient)
    ingredient_mock.get_type.return_value = "SAUCE"
    ingredient_mock.get_name.return_value = "hot sauce"
    ingredient_mock.get_price.return_value = 50
    return ingredient_mock


@pytest.fixture
def mock_ingredient_filling():
    """Фикстура: мок ингредиента типа начинка"""
    ingredient_mock = Mock(spec=Ingredient)
    ingredient_mock.get_type.return_value = "FILLING"
    ingredient_mock.get_name.return_value = "cutlet"
    ingredient_mock.get_price.return_value = 75
    return ingredient_mock


@pytest.fixture
def mock_ingredients(mock_ingredient_sauce, mock_ingredient_filling):
    """Фикстура: список из двух мок-ингредиентов"""
    return [mock_ingredient_sauce, mock_ingredient_filling]
