from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket

from main import app
from testing.helpers.generate_token import MOCK_TOKEN_BENJA

client = TestClient(app)

def test_websocket():
    with client.websocket_connect(
        f"/matches/ws/follow-lobby/55?token={MOCK_TOKEN_BENJA}"
    ) as websocket:
        websocket.send_text("Hello there")