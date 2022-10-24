from fastapi.testclient import TestClient
from pony.orm import db_session
from passlib.hash import bcrypt

from main import app
from database.models.models import User, db

client = TestClient(app)

db.drop_all_tables(with_all_data=True)
db.create_tables()

# Add some users to the database
def fill_users_table():
    users = [
        ('bas_benja', 'basbenja3@gmail.com', 'Compuamigos2', 555888, True),
        ('juliolcese', 'juliolcese@mi.unc.edu.ar', '1whileTrue1', 889654, False),
        ('tonimondejar', 'mondejarantonio@hotmail.com', 'FAMAFyC2022', 123456, True),
        ('valennegrelli', 'valen57negrelli@yahoo.com.ar', 'piXies18', 852436, False),
        ('sebagiraudo', 'sebagir4udo@unc.edu.ar', 'B_1kerfuliate', 785364, True),
        ('lucasca22ina', 'cassinalucas@gmail.com', 'chicosSSS1456', 152347, True),
        ('israangulo4', 'isra1234@hotmail.com', 'Argentiña222', 853314, False)
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

# Try logging in with inexistent username
def test_inexistent_user():
    fill_users_table() # Fill it only once in the first test
    print('\n***** TEST INEXISTENT USER *****')
    response = client.post(
        '/login',
        json = {
            'username_or_email': 'basbenja3',
            'password': 'password' 
        }
    )
    
    print(response.json())
    print('\n')
    assert response.status_code == 401
    assert response.json() == {
        'detail': 'inexistent user'
    }

# Try logging in with wrong password
def test_invalid_credentials():
    print('***** TEST WRONG PASSWORD *****')
    response = client.post(
        '/login',
        json = {
            'username_or_email': 'sebagiraudo',
            'password': 'password' 
        }
    )
    
    print(response.json())
    print('\n')
    assert response.status_code == 401
    assert response.json() == {
        'detail': 'invalid credentials'
    }

# Not verified user tries to log in
def test_not_verified_user():
    print('***** TEST NOT VERIFIED USER *****')
    response = client.post(
        '/login',
        json = {
            'username_or_email': 'israangulo4',
            'password': 'Argentiña222' 
        }
    )
    
    print(response.json())
    print('\n')
    assert response.status_code == 401
    assert response.json() == {
        'detail': 'Not verified user.'
    }

# Logging in with username and correct password
# Get token in return
def test_login_username():
    print('***** TEST LOGIN WITH USERNAME *****')
    response = client.post(
        '/login',
        json = {
            'username_or_email': 'bas_benja',
            'password': 'Compuamigos2' 
        }
    )
    
    print(response.json())
    print('\n')
    assert response.json()['Authorization'] is not None
    assert response.status_code == 200

# Logging in with email and correct password
# Get token in return
def test_login_email():
    print('***** TEST LOGIN WITH EMAIL *****')
    response = client.post(
        '/login',
        json = {
            'username_or_email': 'mondejarantonio@hotmail.com',
            'password': 'FAMAFyC2022'
        }
    )
    
    print(response.json())
    print('\n') 
    assert response.json()['Authorization'] is not None
    assert response.status_code == 200
