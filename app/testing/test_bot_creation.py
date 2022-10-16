from fastapi.testclient import TestClient
from generate_token import MOCK_TOKEN_VALEN, MOCK_TOKEN_JULI
from main import app
from pony.orm import db_session
from database.models.models import User, Robot
from database.dao.user_dao import get_user_by_email
from passlib.hash import bcrypt

client = TestClient(app)

# Add some users to the database
users = [
    ('bas_benja', 'basbenja3@gmail.com', 'Compuamigos2', 555888, False),
    ('juliolcese', 'juliolcese@mi.unc.edu.ar', '1whileTrue1', 889654, True),
    ('tonimondejar', 'mondejarantonio@hotmail.com', 'FAMAFyC2022', 123456, True),
    ('valennegrelli', 'valen57negrelli@yahoo.com.ar', 'piXies18', 852436, True),
    ('sebagiraudo', 'sebagir4udo@unc.edu.ar', '15B_ikerfuliate', 785364, True),
    ('lucasca22ina', 'cassinalucas@gmail.com', 'Loschicos1456', 152347, True),
    ('israangulo4', 'isra1234@hotmail.com', 'Argentina222', 853314, False)
]
with db_session:
    for username, email, password, verification_code, verified in users:
        User(
            username=username,
            email=email,
            hashed_password=bcrypt.hash(password),
            verification_code=verification_code,
            verified=verified
        )

MOCK_SOURCE_CODE = """aW1wb3J0IHV2aWNvcm4KCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgog
                      ICAgdXZpY29ybi5ydW4oImFwcC5hcGk6YXBwIiwgaG9zdD0iMC4wLjAuMCIs
                      IHBvcnQ9ODAwMCwgcmVsb2FkPVRydWUp"""
MOCK_AVATAR = """iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQ
                 DwAEhQGAhKmMIQAAAABJRU5ErkJggg=="""
                 
# Add some robots to the database
robots = [
    ('robot_cool', MOCK_SOURCE_CODE, 'isra1234@hotmail.com', MOCK_AVATAR),
    ('world_destroyer_29', MOCK_SOURCE_CODE, 'cassinalucas@gmail.com', MOCK_AVATAR),
    ('R2D2', MOCK_SOURCE_CODE, 'valen57negrelli@yahoo.com.ar', MOCK_AVATAR),
    ('WALL-E', MOCK_SOURCE_CODE, 'valen57negrelli@yahoo.com.ar', MOCK_AVATAR),
    ('jarvis22', MOCK_SOURCE_CODE, 'valen57negrelli@yahoo.com.ar', MOCK_AVATAR),
    ('_theTERMINATOR', MOCK_SOURCE_CODE, 'cassinalucas@gmail.com', MOCK_AVATAR),
    ('0ptimusPrime', MOCK_SOURCE_CODE, 'basbenja3@gmail.com', MOCK_AVATAR),
    ('CYborg34', MOCK_SOURCE_CODE, 'mondejarantonio@hotmail.com', MOCK_AVATAR),
    ('automatax', MOCK_SOURCE_CODE, 'juliolcese@mi.unc.edu.ar', MOCK_AVATAR)
]
with db_session:
    for robot_name, source_code, owner_email, avatar in robots:
        Robot(
            name=robot_name,
            source_code=source_code,
            owner=get_user_by_email(owner_email),
            avatar=avatar
        )

# Try creating a bot that already exists in the database
def test_create_existent_bot():
    print('***** CREATE EXISTENT BOT *****')
    response = client.post(
        '/create-bot',
        headers={'Authorization': MOCK_TOKEN_VALEN},
        json = {
            'name': 'jarvis22',
            'source_code': MOCK_SOURCE_CODE,
            'avatar': MOCK_AVATAR
        }
    )
    
    print(response.json())
    print('\n')
    assert response.status_code == 409
    assert response.json() == {
        'detail': "User already has a bot with this name."
    }

# Create new bot succesfully
def test_create_bot():
    print('***** CREATE NEW BOT *****')
    response = client.post(
        '/create-bot',
        headers={'Authorization': MOCK_TOKEN_JULI},
        json = {            
            'name': 'R2D2',
            'source_code': MOCK_SOURCE_CODE,
            'avatar': MOCK_AVATAR
        }
    )
    
    print(response.json())
    print('\n')
    assert response.status_code == 200
    assert response.json() == {
        'name': 'R2D2',
        'source_code': MOCK_SOURCE_CODE,
        'avatar': MOCK_AVATAR
    }

