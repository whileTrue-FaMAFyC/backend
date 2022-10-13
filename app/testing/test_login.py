from fastapi.testclient import TestClient
from app.main import app
from app.utils import user_utils

client = TestClient(app)

SECRET_KEY = "2c329a8eca7d0c2ff68d261ad0b2e3efa66cc2603183fe6d0b4b219a11138c84"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440 # One day

# Try logging in with inexistent username
def test_inexistent_user():
    response = client.post(
        "/login",
        json = {
            "username_or_email": "basbenja3",
            "password": "password" 
        }
    )
    
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid credentials"
    }

# Try logging in with wrong password
def test_invalid_credentials():
    response = client.post(
        "/login",
        json = {
            "username_or_email": "madCardinal3",
            "password": "compuamigos" 
        }
    )
    
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid credentials"
    }

# Not verified user tries to log in
def test_not_verified_user():
    response = client.post(
        "/login",
        json = {
            "username_or_email": "cheerfulQuiche6",
            "password": "cheerfulQuiche6" 
        }
    )
    
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not verified user"
    }

# Logging in with username and correct password
# Get token in return
def test_login_username():
    response = client.post(
        "/login",
        json = {
            "username_or_email": "mellowBuzzard1",
            "password": "mellowBuzzard1" 
        }
    )
    
    assert response.headers["Authorization"] is not None
    assert response.status_code == 200

# Logging in with email and correct password
# Get token in return
def test_login_email():
    response = client.post(
        "/login",
        json = {
            "username_or_email": "worriedCockatoo4@hotmail.com",
            "password": "worriedCockatoo4" 
        }
    )
        
    assert response.headers["Authorization"] is not None
    assert response.status_code == 200