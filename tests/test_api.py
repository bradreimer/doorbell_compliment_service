import os
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_compliment_endpoint():
    sample_path = os.path.join(os.path.dirname(__file__), "sample.jpg")

    with open(sample_path, "rb") as f:
        response = client.post(
            "/compliment",
            files={"file": ("sample.jpg", f, "image/jpeg")}
        )

    assert response.status_code == 200
    data = response.json()
    assert "compliment" in data
    assert isinstance(data["compliment"], str)
    assert len(data["compliment"]) > 0

