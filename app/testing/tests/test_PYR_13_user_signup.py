from fastapi.testclient import TestClient

from database.dao.user_dao import *
from testing.helpers.user_helpers import *
from database.models.models import db
from main import app

client = TestClient(app)

def test_successful_sign_up():
    # Deletes the database
    db.drop_all_tables(with_all_data=True)
    db.create_tables()

    response = client.post(
        "/signup",
        json={"username": "tonimondejar", "email": "antoniomondejar2001@gmail.com",
        "password": "Test1234", "avatar": "data:image/png;fake_avatar", "avatarFilename": "fake.png"}
    )

    assert response.status_code == 201

    user = get_user_by_username("tonimondejar")
    # Check if the user was correctly added to the database
    assert user != None
    
    # Must be a hashed password
    assert user.hashed_password != "Test1234" 

    assert user.verified == False
    
    # The filename was correctly concatenated with its content.
    assert user.avatar.startswith("name:fake.png;")

    assert delete_user_by_username("tonimondejar")

def test_successful_sign_up_without_avatar():
    # Deletes the database
    db.drop_all_tables(with_all_data=True)
    db.create_tables()

    response = client.post(
        "/signup",
        json={"username": "tonimondejar", "email": "antoniomondejar2001@gmail.com",
        "password": "Test1234"}
    )

    assert response.status_code == 201
    user = get_user_by_username("tonimondejar")
 
    # Check if the user was correctly added to the database
    assert user != None

    # Must be an empty avatar
    assert user.avatar == "" 

    assert delete_user_by_username("tonimondejar")

def test_username_already_in_use():
    # Deletes the database
    db.drop_all_tables(with_all_data=True)
    db.create_tables()

    response = client.post(
        "/signup",
        json={"username": "tonimondejar", "email": "antoniomondejar2001@gmail.com",
        "password": "Test1234", "avatar": "data:image/png;fake_avatar", "avatarFilename": "fake.png"}
    )

    # User registered correctly
    assert response.status_code == 201
    # Check if user was added to the database
    assert get_user_by_username("tonimondejar") != None

    response = client.post(
        "/signup",
        json={"username": "tonimondejar", "email": "antonio.mondejar@mi.unc.edu.ar",
        "password": "Test1234", "avatar": "data:image/png;fake_avatar", "avatarFilename": "fake.png"}
    )

    # Must fail because username is already in use.
    assert response.status_code == 409
    assert response.json()["detail"] == "Username already in use."
    
    #Checks that the user was not added to the database
    assert get_user_by_email("antonio.mondejar@mi.unc.edu.ar") == None

    # Deletes the first user added
    assert delete_user_by_username("tonimondejar")

def test_email_already_in_use():
    # Deletes the database
    db.drop_all_tables(with_all_data=True)
    db.create_tables()

    response = client.post(
        "/signup",
        json={"username": "tonimondejar", "email": "antoniomondejar2001@gmail.com",
        "password": "Test1234", "avatar": "data:image/png;fake_avatar", "avatarFilename": "fake.png"}
    )
    
    # User registered correctly
    assert response.status_code == 201
    # Check if user was added to the database
    assert get_user_by_username("tonimondejar") != None
    
    response = client.post(
        "/signup",
        json={"username": "tonimondejar1", "email": "antoniomondejar2001@gmail.com",
        "password": "Test1234", "avatar": "data:image/png;fake_avatar", "avatarFilename": "fake.png"}
    )

    # Must fail because email is already in use.
    assert response.status_code == 409
    assert response.json()["detail"] == "Email already associated with another user."

    # Checks that the user was not added to the database
    assert get_user_by_username("tonimondejar1") == None
    
    # Deletes the first user added
    assert delete_user_by_username("tonimondejar")

def test_email_not_valid():
    # Deletes the database
    db.drop_all_tables(with_all_data=True)
    db.create_tables()

    response = client.post(
        "/signup",
        json={"username": "tonimondejar", "email": "antoniomondejzxckzck",
        "password": "Test1234", "avatar": "data:image/png;fake_avatar", "avatarFilename": "fake.png"}
    )

    # Must fail because email is not valid.
    assert response.status_code == 400
    assert response.json()["detail"] == "Email not valid."

    # Checks that the user was not added to the database
    assert get_user_by_username("tonimondejar") == None

def test_password_format_not_valid():
    # Deletes the database
    db.drop_all_tables(with_all_data=True)
    db.create_tables()

    response = client.post(
        "/signup",
        json={"username": "tonimondejar", "email": "antoniomondejar2001@gmail.com",
        "password": "test", "avatar": "data:image/png;fake_avatar", "avatarFilename": "fake.png"} 
    )
    #Missing numbers and capital letters, also its length is less than 8

    # Must fail because password format is not valid.
    assert response.status_code == 400
    assert response.json()["detail"] == "Password format not valid."
    
    # Checks that the user was not added to the database
    assert get_user_by_username("tonimondejar") == None

def test_wrong_avatar_file_extension():
    # Deletes the database
    db.drop_all_tables(with_all_data=True)
    db.create_tables()

    response = client.post(
        "/signup",
        json={"username": "tonimondejar", "email": "antoniomondejar2001@gmail.com",
        "password": "Test1234", "avatar": "data:image/jpeg;fake_avatar", "avatarFilename": "fake.jpeg"}
    )
    
    # Must fail because avatar format is not valid.
    assert response.status_code == 400
    assert response.json()["detail"] == "Avatar extension file not supported."
    
    # Checks that the user was not added to the database
    assert get_user_by_username("tonimondejar") == None
