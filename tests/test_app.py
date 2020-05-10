import pytest
from unittest.mock import patch, MagicMock
from app import get_app

@pytest.fixture
@patch('app.database.Client')
@patch('app.database.os.environ', {"DB_ID": "id", "DB_TABLE": "table"})
def client(db):
    app = get_app()
    app.config['TESTING'] = True
    app.config.dbMock = db

    return app.test_client()

def test_add_message(client):
    rev = client.post("/message",
                      json={"recipient": "a@google.com",
                            "message": "a"})
    assert rev.status_code == 201

def test_invalid_email(client):
    rev = client.post("/message",
                      json={"recipient": "aasdasd",
                            "message": "a"})
    assert rev.status_code == 400

def test_no_args(client):
    rev = client.post("/message")
    assert rev.status_code == 400

def test_get_values(client):
    rev = client.get("/message")
    assert rev.status_code == 200

def test_get_by_index(client):
    rev = client.get("/message?start=0&end=0")
    assert rev.status_code == 200
