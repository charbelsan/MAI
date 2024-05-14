from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_audio():
    with open("path_to_audio_file", "rb") as audio_file:
        response = client.post("/api/v1/chat/", files={"file": audio_file}, data={
            "user_id": 1,
            "target_lang": "en"
        })
    assert response.status_code == 200
    assert "response" in response.json()
    assert "session_id" in response.json()
