from random import randint
from fastapi.testclient import TestClient

from database.dao.user_dao import *
from main import app

client = TestClient(app)


def test_successful_verification():
    response = client.put(
        "/verifyuser/tonimondejar",
        json={
            "verification_code": 123456
        }
    )

    assert response.status_code == 200
    user = get_user_by_username("tonimondejar")
    
    # Checks if the verified attribute was correctly updated
    assert user.verified == True


def test_wrong_verification_code():    
    response = client.put(
        "/verifyuser/tonimondejar",
        json={
            "verification_code": 123457
        }
    )

    assert response.status_code == 400

    # Must fail because verification code is wrong
    assert response.json()["detail"] == "Wrong verification code."

    # Checks if the verified attribute was not updated
    assert get_user_by_username("tonimondejar").verified == False

def test_user_not_registered():    
    random_code = randint(100000,999999)

    response = client.put(
        "/verifyuser/userNotInDb",
        json={
            "verification_code": random_code
        }
    )

    assert response.status_code == 401

    # Must fail because the username does not exist in the database
    assert response.json()["detail"] == "User not registered."


def test_user_already_verified():  
    response = client.put(
        "/verifyuser/bas_benja",
        json={
            "verification_code": 555888
        }
    )

    assert response.status_code == 409

    # Must fail because the user is already verified
    assert response.json()["detail"] == "User already verified."