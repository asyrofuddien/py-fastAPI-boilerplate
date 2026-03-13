import pytest
from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_get_productss():
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
