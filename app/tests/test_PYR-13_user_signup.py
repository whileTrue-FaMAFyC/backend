from ast import Pass
from fastapi.testclient import TestClient
from app.main import app
from database.crud.user import *

client = TestClient(app)

def test_successful_sign_up():
    response = client.post(
        "/signup",
        json={"username": "tonimondejar", "email": "antoniomondejar2001@gmail.com",
        "password": "Test1234"}
    )
    assert response.status_code == 201
    # Must be a hashed password
    assert response.json()["hashed_password"] != "Test1234" 

    assert response.json()["verified"] == False

    user_in_db = get_user_by_username("tonimondejar")
    # Check if the user was added to the database
    assert user_in_db != None

    assert delete_user_by_username("tonimondejar")

def test_username_already_in_use():
    response = client.post(
        "/signup",
        json={"username": "tonimondejar", "email": "antoniomondejar2001@gmail.com",
        "password": "Test1234"}
    )
    # User registered correctly
    assert response.status_code == 201

    response = client.post(
        "/signup",
        json={"username": "tonimondejar", "email": "antonio.mondejar@mi.unc.edu.ar",
        "password": "Test1234"}
    )
    # Must fail because username is already in use.
    assert response.status_code == 400
    assert response.json()["detail"] == "username already in use"

    assert delete_user_by_username("tonimondejar")

def test_email_already_in_use():
    response = client.post(
        "/signup",
        json={"username": "tonimondejar", "email": "antoniomondejar2001@gmail.com",
        "password": "Test1234"}
    )
    # User registered correctly
    assert response.status_code == 201

    response = client.post(
        "/signup",
        json={"username": "tonimondejar1", "email": "antoniomondejar2001@gmail.com",
        "password": "Test1234"}
    )
    # Must fail because email is already in use.
    assert response.status_code == 400
    assert response.json()["detail"] == "email already associated with another user"

    assert delete_user_by_username("tonimondejar")
    # Checks that the user was not added to the database
    assert get_user_by_username("tonimondejar1") == None

def test_email_not_valid():
    response = client.post(
        "/signup",
        json={"username": "tonimondejar1", "email": "antoniomondejar2asdhjash",
        "password": "Test1234"}
    )
    # Must fail because email is not valid.
    assert response.status_code == 400
    assert response.json()["detail"] == "email not valid"

    # Checks that the user was not added to the database
    assert get_user_by_username("tonimondejar1") == None

def test_password_format_not_valid():
    response = client.post(
        "/signup",
        json={"username": "tonimondejar1", "email": "antoniomondejar2001@gmail.com",
        "password": "test"} #Missing numbers and capital letters, also its length is less than 8
    )
    # Must fail because password format is not valid.
    assert response.status_code == 400
    assert response.json()["detail"] == "password format not valid"
    
    # Checks that the user was not added to the database
    assert get_user_by_username("tonimondejar1") == None


## TO DO
def test_wrong_avatar_file_extension():
    pass

# BROKEN, if the email does not exists the system puts the user info into the database anyway.
# the library being used does not tell you if the email was received.
def test_non_existent_email(): 
    response = client.post(
        "/signup",
        json={"username": "tonimondejar1", "email": "antomondejarnoexisteniahi@gmail.com",
        "password": "Test1234"}
    )
    # Must fail because email does not exists.
    assert response.status_code == 500
    # assert response.json()["detail"] == "internal error sending the email with the verification code"
    
    # Checks that the user was not added to the database
    assert get_user_by_username("tonimondejar1") == None