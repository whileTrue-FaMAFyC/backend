from fastapi.testclient import TestClient

from database.dao.match_dao import delete_table_match
from database.dao.robot_dao import delete_table_robot
from database.dao.user_dao import *
from main import app

client = TestClient(app)

def test_successful_sign_up():
    # Deletes the database
    assert delete_table_user()
    assert delete_table_robot()
    assert delete_table_match()

    response = client.post(
        "/signup",
        json={"username": "tonimondejar", "email": "antoniomondejar2001@gmail.com",
        "password": "Test1234", "avatar": "data:image/png;fake_avatar", "avatarFilename": "fake.png"}
    )

    assert response.status_code == 201
    # Must be a hashed password
    assert response.json()["hashed_password"] != "Test1234" 

    assert response.json()["verified"] == False
    # The filename was correctly concatenated with its content.
    assert response.json()["avatar"].startswith("name:fake.png;")
    # Check if the user was correctly added to the database
    assert get_user_by_username("tonimondejar") != None

    assert delete_user_by_username("tonimondejar")

def test_successful_sign_up_without_avatar():
    # Deletes the database
    assert delete_table_user()
    assert delete_table_robot()
    assert delete_table_match()

    response = client.post(
        "/signup",
        json={"username": "tonimondejar", "email": "antoniomondejar2001@gmail.com",
        "password": "Test1234"}
    )

    assert response.status_code == 201
    # Must be an empty avatar
    assert response.json()["avatar"] == "" 

    # Check if the user was correctly added to the database
    assert get_user_by_username("tonimondejar") != None

    assert delete_user_by_username("tonimondejar")

def test_username_already_in_use():
    # Deletes the database
    assert delete_table_user()
    assert delete_table_robot()
    assert delete_table_match()

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
    assert response.status_code == 400
    assert response.json()["detail"] == "username already in use"
    
    #Checks that the user was not added to the database
    assert get_user_by_email("antonio.mondejar@mi.unc.edu.ar") == None

    # Deletes the first user added
    assert delete_user_by_username("tonimondejar")

def test_email_already_in_use():
    # Deletes the database
    assert delete_table_user()
    assert delete_table_robot()
    assert delete_table_match()

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
    assert response.status_code == 400
    assert response.json()["detail"] == "email already associated with another user"

    # Checks that the user was not added to the database
    assert get_user_by_username("tonimondejar1") == None
    
    # Deletes the first user added
    assert delete_user_by_username("tonimondejar")

def test_email_not_valid():
    # Deletes the database
    assert delete_table_user()
    assert delete_table_robot()
    assert delete_table_match()

    response = client.post(
        "/signup",
        json={"username": "tonimondejar", "email": "antoniomondejzxckzck",
        "password": "Test1234", "avatar": "data:image/png;fake_avatar", "avatarFilename": "fake.png"}
    )

    # Must fail because email is not valid.
    assert response.status_code == 400
    assert response.json()["detail"] == "email not valid"

    # Checks that the user was not added to the database
    assert get_user_by_username("tonimondejar") == None

def test_password_format_not_valid():
    # Deletes the database
    assert delete_table_user()
    assert delete_table_robot()
    assert delete_table_match()

    response = client.post(
        "/signup",
        json={"username": "tonimondejar", "email": "antoniomondejar2001@gmail.com",
        "password": "test", "avatar": "data:image/png;fake_avatar", "avatarFilename": "fake.png"} 
    )
    #Missing numbers and capital letters, also its length is less than 8

    # Must fail because password format is not valid.
    assert response.status_code == 400
    assert response.json()["detail"] == "password format not valid"
    
    # Checks that the user was not added to the database
    assert get_user_by_username("tonimondejar") == None

def test_wrong_avatar_file_extension():
    # Deletes the database
    assert delete_table_user()
    assert delete_table_robot()
    assert delete_table_match()

    response = client.post(
        "/signup",
        json={"username": "tonimondejar", "email": "antoniomondejar2001@gmail.com",
        "password": "Test1234", "avatar": "data:image/jpeg;fake_avatar", "avatarFilename": "fake.jpeg"}
    )
    
    # Must fail because avatar format is not valid.
    assert response.status_code == 400
    assert response.json()["detail"] == "avatar extension file not supported"
    
    # Checks that the user was not added to the database
    assert get_user_by_username("tonimondejar") == None

def test_non_existent_email():
    # Deletes the database
    assert delete_table_user()
    assert delete_table_robot()
    assert delete_table_match()

    response = client.post(
        "/signup",
        json={"username": "tonimondejar", "email": "antonionoexisteniahi@gmail.com",
        "password": "Test1234", "avatar": "data:image/png;fake_avatar", "avatarFilename": "fake.png"}
    )

    # Must fail because email does not exists.
    assert response.status_code == 400
    assert response.json()["detail"] == "email does not exist"
    
    # Checks that the user was not added to the database
    assert get_user_by_username("tonimondejar") == None