from fastapi.testclient import TestClient
from app.main import app
from pony.orm import db_session
from database.models.models import User
from passlib.hash import bcrypt

client = TestClient(app)

# Add some users to the database
users = [
    ('bas_benja', 'basbenja3@gmail.com', 'compuamigos2', 555888, True),
    ('juliolcese', 'juliolcese@mi.unc.edu.ar', '1whileTrue1', 889654, False),
    ('tonimondejar', 'mondejarantonio@hotmail.com', 'famafyc2022', 123456, True),
    ('valennegrelli', 'valen57negrelli@yahoo.com.ar', 'pixies18', 852436, False),
    ('sebagiraudo', 'sebagir4udo@unc.edu.ar', 'b_ikerfuliate', 785364, True),
    ('lucasca22ina', 'cassinalucas@gmail.com', 'chicos1456', 152347, True),
    ('israangulo4', 'isra1234@hotmail.com', 'argentina222', 853314, False)
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
        'detail': 'Invalid credentials'
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
        'detail': 'Invalid credentials'
    }

# Not verified user tries to log in
def test_not_verified_user():
    print('***** TEST NOT VERIFIED USER *****')
    response = client.post(
        '/login',
        json = {
            'username_or_email': 'israangulo4',
            'password': 'argentina222' 
        }
    )
    
    print(response.json())
    print('\n')
    assert response.status_code == 401
    assert response.json() == {
        'detail': 'Not verified user'
    }

# Logging in with username and correct password
# Get token in return
def test_login_username():
    print('***** TEST LOGIN WITH USERNAME *****')
    response = client.post(
        '/login',
        json = {
            'username_or_email': 'bas_benja',
            'password': 'compuamigos2' 
        }
    )
    
    print(response.json())
    print('\n')
    print(response.headers['Authorization'])
    print('\n')
    assert response.headers['Authorization'] is not None
    assert response.status_code == 200

# Logging in with email and correct password
# Get token in return
def test_login_email():
    print('***** TEST LOGIN WITH EMAIL *****')
    response = client.post(
        '/login',
        json = {
            'username_or_email': 'mondejarantonio@hotmail.com',
            'password': 'famafyc2022'
        }
    )
    
    print(response.json())
    print('\n')
    print(response.headers['Authorization'])
    print('\n') 
    assert response.headers['Authorization'] is not None
    assert response.status_code == 200