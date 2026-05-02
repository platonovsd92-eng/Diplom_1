import pytest
from unittest.mock import Mock
from praktikum.burger import Burger


class TestBurger:
    """Тесты для класса Burger (100% покрытие)"""

    def test_set_buns_saves_bun(self, mock_bun):
        burger = Burger()
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    def test_add_ingredient_appends_to_list(self, mock_ingredient_sauce):
        burger = Burger()
        burger.add_ingredient(mock_ingredient_sauce)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient_sauce

    @pytest.mark.parametrize("index", [0, 1])
    def test_remove_ingredient_deletes_by_index(self, index, mock_ingredients):
        burger = Burger()
        for ing in mock_ingredients:
            burger.add_ingredient(ing)

        original_length = len(burger.ingredients)
        removed_ingredient = burger.ingredients[index]

        burger.remove_ingredient(index)

        assert len(burger.ingredients) == original_length - 1
        assert removed_ingredient not in burger.ingredients

    @pytest.mark.parametrize("index,new_index", [
        (0, 1),
        (1, 0),
    ])
    def test_move_ingredient_changes_position(self, index, new_index, mock_ingredients):
        burger = Burger()
        for ing in mock_ingredients:
            burger.add_ingredient(ing)

        moved_ingredient = burger.ingredients[index]
        burger.move_ingredient(index, new_index)
        assert burger.ingredients[new_index] == moved_ingredient

    def test_get_price_calculates_with_bun_and_ingredients(self, mock_bun, mock_ingredients):
        mock_bun.get_price.return_value = 100
        mock_ingredients[0].get_price.return_value = 50
        mock_ingredients[1].get_price.return_value = 75

        burger = Burger()
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredients[0])
        burger.add_ingredient(mock_ingredients[1])

        expected_price = 100 * 2 + 50 + 75
        assert burger.get_price() == expected_price

    @pytest.mark.parametrize("bun_price,ingredient_prices,expected", [
        (100, [50, 75], 325),
        (200, [30, 40, 50], 520),
        (50, [], 100),
        (0, [100], 100),
        (150, [10, 20, 30], 360),
    ])
    def test_get_price_parametrized(self, bun_price, ingredient_prices, expected, mock_bun):
        mock_bun.get_price.return_value = bun_price

        burger = Burger()
        burger.set_buns(mock_bun)

        for price in ingredient_prices:
            ingredient = Mock()
            ingredient.get_price.return_value = price
            burger.add_ingredient(ingredient)

        assert burger.get_price() == expected

    def test_get_receipt_returns_correct_format(self, mock_bun, mock_ingredients):
        mock_bun.get_name.return_value = "black bun"
        mock_ingredients[0].get_type.return_value = "SAUCE"
        mock_ingredients[0].get_name.return_value = "hot sauce"
        mock_ingredients[1].get_type.return_value = "FILLING"
        mock_ingredients[1].get_name.return_value = "cutlet"

        burger = Burger()
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredients[0])
        burger.add_ingredient(mock_ingredients[1])

        receipt = burger.get_receipt()

        expected_receipt = (
            '(==== black bun ====)\n'
            '= sauce hot sauce =\n'
            '= filling cutlet =\n'
            '(==== black bun ====)\n\n'
            'Price: 325'
        )

        assert receipt == expected_receipt

    @pytest.mark.parametrize("ingredient_type,expected_type_in_receipt", [
        ("SAUCE", "sauce"),
        ("FILLING", "filling"),
    ])
    def test_get_receipt_handles_different_ingredient_types(self, mock_bun, ingredient_type, expected_type_in_receipt):
        mock_bun.get_name.return_value = "black bun"

        mock_ingredient = Mock()
        mock_ingredient.get_type.return_value = ingredient_type
        mock_ingredient.get_name.return_value = "test ingredient"
        mock_ingredient.get_price.return_value = 100

        burger = Burger()
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient)

        receipt = burger.get_receipt()
        expected_line = f'= {expected_type_in_receipt} test ingredient ='

        assert expected_line in receipt

    def test_get_receipt_without_bun_raises_error(self):
        burger = Burger()
        with pytest.raises(AttributeError):
            burger.get_receipt()

    def test_get_price_without_bun_raises_error(self):
        burger = Burger()
        with pytest.raises(AttributeError):
            burger.get_price()

    def test_add_multiple_ingredients_maintains_order(self, mock_ingredient_sauce, mock_ingredient_filling):
        burger = Burger()
        burger.add_ingredient(mock_ingredient_sauce)
        burger.add_ingredient(mock_ingredient_filling)

        assert burger.ingredients[0] == mock_ingredient_sauce
        assert burger.ingredients[1] == mock_ingredient_filling

    def test_remove_ingredient_out_of_range_raises_error(self, mock_ingredient_sauce):
        burger = Burger()
        burger.add_ingredient(mock_ingredient_sauce)

        with pytest.raises(IndexError):
            burger.remove_ingredient(5)

    def test_move_ingredient_to_valid_position_works(self, mock_ingredients):
        burger = Burger()
        for ing in mock_ingredients:
            burger.add_ingredient(ing)

        original_first = burger.ingredients[0]
        burger.move_ingredient(0, 1)
        assert burger.ingredients[1] == original_first

    def test_set_buns_overwrites_previous_bun(self, mock_bun):
        burger = Burger()
        another_bun = Mock()
        burger.set_buns(mock_bun)
        burger.set_buns(another_bun)
        assert burger.bun == another_bun
        