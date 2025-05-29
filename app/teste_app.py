from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_square():
    response = client.get("/square/3")
    assert response.status_code == 200
    assert response.json() == {"result": 9}

def test_double():
    response = client.get("/double/4")
    assert response.status_code == 200
    assert response.json() == {"result": 8}
