import os.path

import pytest

from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password



pf = PetFriends()

def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter = ''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert  len(result['pets']) > 0

#Новые тесты

def test_get_api_key_for_invalid_user_password(email = valid_email, password = invalid_password):
    """Метод проверяет, что сайт не выдает ключ при вводе неправильного пароля"""
    with pytest.raises(AssertionError):
        status, result = pf.get_api_key(email, password)
        assert status == 200
        assert 'key' in result

def test_get_api_key_for_empty_user_password(email = valid_email, password = ''):
    """Метод проверяет, что сайт не выдает ключ, если оставить поле ввода пароля пустым"""
    with pytest.raises(AssertionError):
        status, result = pf.get_api_key(email, password)
        assert status == 200
        assert 'key' in result

def test_get_api_key_for_invalid_user_email(email = invalid_email, password = invalid_password):
    """Метод проверяет, что сайт не выдает ключ при вводе неправильного e-mail"""
    with pytest.raises(AssertionError):
        status, result = pf.get_api_key(email, password)
        assert status == 200
        assert 'key' in result

def test_get_api_key_for_empty_user_email(email = '', password = invalid_password):
    """Метод проверяет, что сайт не выдает ключ, если оставить поле ввода e-mail пустым"""
    with pytest.raises(AssertionError):
        status, result = pf.get_api_key(email, password)
        assert status == 200
        assert 'key' in result

def test_add_new_pet_without_photo(name = 'Бататуйя', animal_type = 'Улитка', age = '7'):
    """Метод проверяет, добавляется ли питомец при вводе корректных данных"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_set_photo(pet_photo = 'images/giantsnail.jpg'):
    """Метод проверяет, корректно ли добавляется фото питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    if len(my_pets['pets']) > 0:
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception('There is not my pets')

def test_update_pet_information(name = 'Татуйя', animal_type = 'Улитка', age = '10'):
    """Метод проверяет, обновляется ли информация о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_information(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('There is not my pets')


def test_add_new_pet_with_full_valid_data(name = 'Бататуйя', animal_type = 'Улитка', age = '7',
                                     pet_photo = 'images/giantsnail.jpg'):
    """Метод проверяет, добавляется ли питомец при вводе корректных данных с фото"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_delete_pet():
    """Метод проверяет, удаляется ли корректно анкета питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_with_photo(auth_key, name = 'Бататуйя', animal_type = 'Улитка', age = '7',
                                     pet_photo = 'images/giantsnail.jpg')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()

def test_add_new_pet_empty(name = '', animal_type = '', age = ''):
    """Метод проверяет, добавляется ли питомец, если оставить поля ввода данных питомца пустыми"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name