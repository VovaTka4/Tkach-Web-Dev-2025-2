import pytest, re

def test_get_by_id_with_existing_user(user_repository, existing_user):
    user = user_repository.get_by_id(existing_user.id)
    assert user.id == existing_user.id
    assert user.name == existing_user.name
    
def test_get_by_id_with_nonexisting_user(user_repository, nonexisting_user_id):
    user = user_repository.get_by_id(nonexisting_user_id)
    assert user is None

def test_all_with_nonempty_db(user_repository, example_users):
    users = user_repository.all()
    assert len(users) == len(example_users)
    for loaded_user, example_user in zip(users, example_users):
        assert loaded_user.id == example_user.id
        assert loaded_user.name == example_user.name