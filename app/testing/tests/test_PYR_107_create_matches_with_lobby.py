from fastapi.testclient import TestClient

from controllers.match_controller import lobbys
from main import app
from testing.helpers.generate_token import MOCK_TOKEN_BENJA, MOCK_TOKEN_JULI, MOCK_TOKEN_TONI, MOCK_TOKEN_VALEN


tokens = [MOCK_TOKEN_BENJA, MOCK_TOKEN_JULI, MOCK_TOKEN_TONI, MOCK_TOKEN_VALEN]


client = TestClient(app)


# Create lobbys for different matches
def test_various_lobbys():
    mock_matches = [
        (MOCK_TOKEN_BENJA, 'myMatch', 'Bumblebee', 3, 4, 179, 5600, ''),
        (MOCK_TOKEN_JULI, 'myMatch', 'automatax', 2, 4, 65, 200, 'password'),
        (MOCK_TOKEN_TONI, 'tonisMatch', 'MegaByte', 3, 4, 5, 5, '___')
    ]
    
    for (token, name, creator_robot, min_players, max_players, num_games, num_rounds, 
        password) in mock_matches:
        response = client.post(
            "/matches/new-match",
            headers = {'Authorization': token},
            json = {
                'name': name,
                'creator_robot': creator_robot,
                'min_players': min_players,
                'max_players': max_players,
                'num_games': num_games,
                'num_rounds': num_rounds,
                'password': password
            }
        )
        assert response.status_code == 201
    
    assert len(lobbys) == 3
