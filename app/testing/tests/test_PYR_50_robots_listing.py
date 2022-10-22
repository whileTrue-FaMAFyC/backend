from fastapi.testclient import TestClient
from passlib.hash import bcrypt
from pony.orm import db_session

from main import app
from database.dao import user_dao
from database.models.models import db, Robot, User
from testing.helpers.generate_token import MOCK_TOKEN_VALEN
from utils.user_utils import INVALID_TOKEN_EXCEPTION


client = TestClient(app)

MOCK_SOURCE_CODE = """aW1wb3J0IHV2aWNvcm4KCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgog
                      ICAgdXZpY29ybi5ydW4oImFwcC5hcGk6YXBwIiwgaG9zdD0iMC4wLjAuMCIs
                      IHBvcnQ9ODAwMCwgcmVsb2FkPVRydWUp"""

MOCK_AVATAR = """iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQ
                 DwAEhQGAhKmMIQAAAABJRU5ErkJggg=="""

# Add some users to the database
@db_session
def initial_users():
    users = [
        ('bas_benja', 'basbenja3@gmail.com', 'Compuamigos2', 555888, False),
        ('juliolcese', 'juliolcese@mi.unc.edu.ar', '1whileTrue1', 889654, True),
        ('tonimondejar', 'mondejarantonio@hotmail.com', 'FAMAFyC2022', 123456, True),
        ('valennegrelli', 'valen57negrelli@yahoo.com.ar', 'piXies18', 852436, True),
        ('sebagiraudo', 'sebagir4udo@unc.edu.ar', '15B_ikerfuliate', 785364, True),
        ('lucasca22ina', 'cassinalucas@gmail.com', 'Loschicos1456', 152347, True),
        ('israangulo4', 'isra1234@hotmail.com', 'Argentina222', 853314, False)
    ]
    for username, email, password, verification_code, verified in users:
        User(
            username=username,
            email=email,
            hashed_password=bcrypt.hash(password),
            verification_code=verification_code,
            verified=verified
        )

    return

# Add some robots to the database
@db_session
def initial_robots():
    robots = [
        ('robot_cool', MOCK_SOURCE_CODE, 'isra1234@hotmail.com', MOCK_AVATAR),
        ('world_destroyer_29', MOCK_SOURCE_CODE, 'cassinalucas@gmail.com', MOCK_AVATAR),
        ('_theTERMINATOR', MOCK_SOURCE_CODE, 'cassinalucas@gmail.com', MOCK_AVATAR),
        ('0ptimusPrime', MOCK_SOURCE_CODE, 'basbenja3@gmail.com', MOCK_AVATAR),
        ('CYborg34', MOCK_SOURCE_CODE, 'mondejarantonio@hotmail.com', MOCK_AVATAR),
        ('automatax', MOCK_SOURCE_CODE, 'juliolcese@mi.unc.edu.ar', MOCK_AVATAR)
    ]
    for robot_name, source_code, owner_email, avatar in robots:
        Robot(
            name=robot_name,
            source_code=source_code,
            owner=user_dao.get_user_by_email(owner_email),
            avatar=avatar
        )

    return

@db_session
def user_tested_robots():
    robots = [
        ('R2D2', MOCK_SOURCE_CODE, 'valen57negrelli@yahoo.com.ar', MOCK_AVATAR),
        ('WALL-E', MOCK_SOURCE_CODE, 'valen57negrelli@yahoo.com.ar', MOCK_AVATAR),
        ('jarvis22', MOCK_SOURCE_CODE, 'valen57negrelli@yahoo.com.ar', MOCK_AVATAR),
    ]
    for robot_name, source_code, owner_email, avatar in robots:
        Robot(
            name=robot_name,
            source_code=source_code,
            owner=user_dao.get_user_by_email(owner_email),
            avatar=avatar
        )

    return

# Test case where the user has no robots.
def test_no_robots():
    db.drop_all_tables(with_all_data=True)
    db.create_tables()
    initial_users()
    initial_robots()

    response = client.get("/list-robots",
                          headers = {"Authorization": MOCK_TOKEN_VALEN})
    assert response.status_code == 200
    assert response.json() == []
    return

expected_response =  [{"name": "R2D2"}, {"name": "WALL-E"}, {"name": "jarvis22"}]

# In this test we first create new matches and then analyze the behavior.
def test_with_matches():
    user_tested_robots()

    response = client.get("/list-robots",
                          headers = {"Authorization": MOCK_TOKEN_VALEN})

    assert response.status_code == 200
    assert response.json() == expected_response

def test_invalid_token():
    response = client.get("/list-robots",
                          headers = {"Authorization": ""})

    assert response.status_code == INVALID_TOKEN_EXCEPTION.status_code
    assert response.json()["detail"] == INVALID_TOKEN_EXCEPTION.detail