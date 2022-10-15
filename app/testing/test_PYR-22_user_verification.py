from random import randint
from fastapi.testclient import TestClient
from app.database.dao.match_dao import delete_table_match
from app.database.dao.robot_dao import delete_table_robot
from app.main import app
from database.dao.user_dao import *
from view_entities.user_view_entities import NewUserToDb

client = TestClient(app)

def test_successful_verification():
    # Deletes the database
    assert delete_table_user()
    assert delete_table_robot()
    assert delete_table_match()

    code = randint(100000,999999)

    user_to_db = NewUserToDb(username="tonimondejar", email="antoniomondejar2001@gmail.com",
    hashed_password="fake_hash", verification_code=code, verified=False)
    
    # Adds the user to the database and checks if it was correctly added
    assert create_user(user_to_db)

    response = client.put(
        "/verifyuser/tonimondejar",
        json={
            "verification_code":code
        }
    )

    assert response.status_code == 200

    # Checks if the verified attribute was correctly updated
    assert response.json()["verified"] == True

    # Deletes user from the database
    assert delete_user_by_username("tonimondejar")

def test_wrong_verification_code():
    # Deletes the database
    assert delete_table_user()
    assert delete_table_robot()
    assert delete_table_match()
    
    random_code = randint(100000,999999)

    user_to_db = NewUserToDb(username="tonimondejar", email="antoniomondejar2001@gmail.com",
    hashed_password="fake_hash", verification_code=random_code, verified=False)
    
    # Adds the user to the database and checks if it was correctly added
    assert create_user(user_to_db)

    response = client.put(
        "/verifyuser/tonimondejar",
        json={
            "verification_code":random_code + 1
        }
    )

    assert response.status_code == 400

    # Must fail because verification code is wrong
    assert response.json()["detail"] == "wrong verification code"

    # Checks if the verified attribute was not updated
    assert get_user_by_username("tonimondejar").verified == False

    # Deletes user from the database
    assert delete_user_by_username("tonimondejar")

def test_user_not_registered():
    # Deletes the database
    assert delete_table_user()
    assert delete_table_robot()
    assert delete_table_match()
    
    random_code = randint(100000,999999)

    response = client.put(
        "/verifyuser/tonimondejar",
        json={
            "verification_code":random_code
        }
    )

    assert response.status_code == 400

    # Must fail because the username does not exist in the database
    assert response.json()["detail"] == "user not registered"

def test_user_already_verified():
    # Deletes the database
    assert delete_table_user()
    assert delete_table_robot()
    assert delete_table_match()
    
    random_code = randint(100000,999999)

    user_to_db = NewUserToDb(username="tonimondejar", email="antoniomondejar2001@gmail.com",
    hashed_password="fake_hash", verification_code=random_code, verified=True)
    
    # Adds the user to the database and checks if it was correctly added
    assert create_user(user_to_db)

    response = client.put(
        "/verifyuser/tonimondejar",
        json={
            "verification_code":random_code
        }
    )

    assert response.status_code == 400

    # Must fail because the user is already verified
    assert response.json()["detail"] == "user already verified"

    # Deletes user from the database
    assert delete_user_by_username("tonimondejar")
