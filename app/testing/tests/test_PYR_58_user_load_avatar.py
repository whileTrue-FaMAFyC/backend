from fastapi.testclient import TestClient

from database.dao.user_dao import *
from testing.helpers.user_helpers import *
from database.models.models import db
from main import app

client = TestClient(app)

def test_successful_load_not_default_avatar():
    # Deletes the database
    db.drop_all_tables(with_all_data=True)
    db.create_tables()

    user_to_db = NewUserToDb(username="tonimondejar", email="antoniomondejar2001@gmail.com",
    hashed_password="fake_hash", verification_code=123456, verified=True)

    # Adds the user to the database and checks if it was correctly added
    assert create_user(user_to_db)

    response = client.post(
        "/load-avatar/tonimondejar",
        json={"avatar": "data:image/png;not_default"}
    )

    assert response.status_code == 200

    assert get_user_by_username("tonimondejar").avatar == "data:image/png;not_default"

    assert delete_user_by_username("tonimondejar")

def test_successful_load_default_avatar():
    # Deletes the database
    db.drop_all_tables(with_all_data=True)
    db.create_tables()

    user_to_db = NewUserToDb(username="tonimondejar", email="antoniomondejar2001@gmail.com",
    hashed_password="fake_hash", verification_code=123456, verified=True)

    # Adds the user to the database and checks if it was correctly added
    assert create_user(user_to_db)

    response = client.post(
        "/load-avatar/tonimondejar",
        json={"avatar": ""}
    )

    assert response.status_code == 200

    assert get_user_by_username("tonimondejar").avatar == "default"

    assert delete_user_by_username("tonimondejar")

def test_user_not_registered():
    # Deletes the database
    db.drop_all_tables(with_all_data=True)
    db.create_tables()

    response = client.post(
        "/load-avatar/tonimondejar",
        json={"avatar": "fake_default", "avatarFilename": "default.png"}
    )

    assert response.status_code == 401

    # Must fail because the username does not exist in the database
    assert response.json()["detail"] == "User not registered."

def test_user_not_verified():
    # Deletes the database
    db.drop_all_tables(with_all_data=True)
    db.create_tables()

    user_to_db = NewUserToDb(username="tonimondejar", email="antoniomondejar2001@gmail.com",
    hashed_password="fake_hash", verification_code=123456, verified=False)
    
    # Adds the user to the database and checks if it was correctly added
    assert create_user(user_to_db)

    response = client.post(
        "/load-avatar/tonimondejar",
        json={"avatar": "fake_default", "avatarFilename": "default.png"}
    )

    assert response.status_code == 401

    # Must fail because the user is not verified.
    assert response.json()["detail"] == "Not verified user."
    
    assert delete_user_by_username("tonimondejar")

def test_avatar_already_loaded():
    # Deletes the database
    db.drop_all_tables(with_all_data=True)
    db.create_tables()

    user_to_db = NewUserToDb(username="tonimondejar", email="antoniomondejar2001@gmail.com",
    hashed_password="fake_hash", verification_code=123456, verified=True, avatar="fake_avatar")
    
    # Adds the user to the database and checks if it was correctly added
    assert create_user(user_to_db)

    response = client.post(
        "/load-avatar/tonimondejar",
        json={"avatar": "fake_default", "avatarFilename": "default.png"}
    )

    assert response.status_code == 403
    # Must fail because the avatar was already loaded (it is "fake_avatar")
    assert response.json()["detail"] == "Avatar already loaded."

    assert get_user_by_username("tonimondejar").avatar == "fake_avatar"

    assert delete_user_by_username("tonimondejar")

def test_avatar_format_not_valid():
    # Deletes the database
    db.drop_all_tables(with_all_data=True)
    db.create_tables()

    user_to_db = NewUserToDb(username="tonimondejar", email="antoniomondejar2001@gmail.com",
    hashed_password="fake_hash", verification_code=123456, verified=True)
    
    # Adds the user to the database and checks if it was correctly added
    assert create_user(user_to_db)

    response = client.post(
        "/load-avatar/tonimondejar",
        json={"avatar": "data:python-x/fake_default", "avatarFilename": "default.png"}
    )

    assert response.status_code == 415
    # Must fail because the avatar was already loaded (it is "fake_avatar")
    assert response.json()["detail"] == "Avatar extension file not supported."

    assert delete_user_by_username("tonimondejar")