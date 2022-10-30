from fastapi.testclient import TestClient

from database.dao.user_dao import *
from testing.helpers.user_helpers import *
from main import app

client = TestClient(app)

def test_successful_sign_up():
    response = client.post(
        "/signup",
        json={
            "username": "jakeperalta", 
            "email": "pyrobots.notreply@gmail.com",
            "password": "Test1234"
        }
    )

    assert response.status_code == 201

    user = get_user_by_username("jakeperalta")
    
    # Check if the user was correctly added to the database
    assert user != None
    
    # Must be a hashed password
    assert user.hashed_password != "Test1234" 
    
    assert user.verified == False


def test_username_already_in_use():
    response = client.post(
        "/signup",
        json={
            "username": "jakeperalta", 
            "email": "pyrobots.notreply@gmail.com",
            "password": "Test1234"
        }
    )

    # User registered correctly
    assert response.status_code == 201
    # Check if user was added to the database
    assert get_user_by_username("jakeperalta") != None

    response = client.post(
        "/signup",
        json={
            "username": "jakeperalta", 
            "email": "pyrobots@gmail.com",
            "password": "Test1234"
        }
    )

    # Must fail because username is already in use.
    assert response.status_code == 409
    assert response.json()["detail"] == "Username already in use."
    
    #Checks that the user was not added to the database
    assert get_user_by_email("pyrobots@gmail.com") == None


def test_email_already_in_use():
    response = client.post(
        "/signup",
        json={
            "username": "jakeperalta", 
            "email": "pyrobots.notreply@gmail.com",
            "password": "Test1234"
        }
    )
    
    # User registered correctly
    assert response.status_code == 201
    # Check if user was added to the database
    assert get_user_by_username("jakeperalta") != None
    
    response = client.post(
        "/signup",
        json={
            "username": "jakeperalta1", 
            "email": "pyrobots.notreply@gmail.com",
            "password": "Test1234"
        }
    )

    # Must fail because email is already in use.
    assert response.status_code == 409
    assert response.json()["detail"] == "Email already associated with another user."

    # Checks that the user was not added to the database
    assert get_user_by_username("jakeperalta1") == None


def test_email_not_valid():
    response = client.post(
        "/signup",
        json={
            "username": "jakeperalta", 
            "email": "antoniomondejzxckzck",
            "password": "Test1234"
        }
    )

    # Must fail because email is not valid.
    assert response.status_code == 400
    assert response.json()["detail"] == "Email not valid."


def test_password_format_not_valid():
    response = client.post(
        "/signup",
        json={
            "username": "jakeperalta", 
            "email": "pyrobots.notreply@gmail.com",
            "password": "test"
        } 
    )
    #Missing numbers and capital letters, also its length is less than 8

    # Must fail because password format is not valid.
    assert response.status_code == 400
    assert response.json()["detail"] == "Password format not valid."