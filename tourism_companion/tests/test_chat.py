from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat():
    response = client.post("/api/v1/chat/", json={
        "text": "Hello, how are you?",
        "user_id": 1,
        "target_lang": "en"
    })
    assert response.status_code == 200
    assert "response" in response.json()
    assert "session_id" in response.json()
