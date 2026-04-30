import sys
import os
from unittest.mock import MagicMock

# Получаем путь к корню проекта
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# СОЗДАЁМ ФЕЙКОВЫЙ МОДУЛЬ praktikum ДО ЛЮБЫХ ИМПОРТОВ
class PraktikumModule:
    pass

# Создаём и регистрируем модуль praktikum
praktikum = PraktikumModule()
sys.modules['praktikum'] = praktikum

# Создаём фейковые подмодули
for submodule in ['bun', 'burger', 'ingredient', 'ingredient_types', 'database']:
    fake_module = MagicMock()
    sys.modules[f'praktikum.{submodule}'] = fake_module
    setattr(praktikum, submodule, fake_module)


# Добавляем путь к корню
sys.path.insert(0, project_root)

import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_bun():
    """Фикстура: мок булочки"""
    bun_mock = Mock()
    bun_mock.get_name.return_value = "black bun"
    bun_mock.get_price.return_value = 100
    return bun_mock


@pytest.fixture
def mock_ingredient_sauce():
    """Фикстура: мок ингредиента типа соус"""
    ingredient_mock = Mock()
    ingredient_mock.get_type.return_value = "SAUCE"
    ingredient_mock.get_name.return_value = "hot sauce"
    ingredient_mock.get_price.return_value = 50
    return ingredient_mock


@pytest.fixture
def mock_ingredient_filling():
    """Фикстура: мок ингредиента типа начинка"""
    ingredient_mock = Mock()
    ingredient_mock.get_type.return_value = "FILLING"
    ingredient_mock.get_name.return_value = "cutlet"
    ingredient_mock.get_price.return_value = 75
    return ingredient_mock


@pytest.fixture
def mock_ingredients(mock_ingredient_sauce, mock_ingredient_filling):
    """Фикстура: список из двух мок-ингредиентов"""
    return [mock_ingredient_sauce, mock_ingredient_filling]
