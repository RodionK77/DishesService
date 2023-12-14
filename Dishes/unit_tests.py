
import DishesService

expected_dishes = [{'id': 1, 'name': 'dish1', 'price': 10}, {'id': 2, 'name': 'dish2', 'price': 3},
                {'id': 3, 'name': 'dish3', 'price': 5}]

expected_dish = {'id': 2, 'name': 'dish2', 'price': 3}

expected_order = {'id': 2, 'customer_id': 1, 'total_price': 20}

def test_get_all_dishes(mocker):
    mocker.patch('DishesService.get_all_dishes_from_db', return_value = expected_dishes)
    result = DishesService.get_all_dishes_from_db()
    assert(result == expected_dishes)

def test_get_dish_by_id(mocker):
    mocker.patch('DishesService.get_dishes_by_id_from_db', return_value = expected_dish)
    result = DishesService.get_dishes_by_id_from_db(2)
    assert(result == expected_dish)

def test_confirm_order(mocker):
    mocker.patch('DishesService.get_order_by_id_from_db', return_value = expected_order)
    result = DishesService.confirm_order(2, 1)
    assert (result == "Order 2 for client 1 confirmed. Total price: 20")

def test_bad_confirm_order(mocker):
    mocker.patch('DishesService.get_order_by_id_from_db', return_value = None)
    result = DishesService.confirm_order(2, 1)
    assert (result == "Order 2 not found.")