from app import schemas
from .database import client, session
import pytest


# def test_root(client):
#     res = client.get("/")
#     print(res.json())
#     assert res.json().get("message") == "Hello world"
#     assert res.status_code == 200

@pytest.fixture
def test_user(client):
    user_data = {"email":"khang@gmail.com",
                 "password": "khang1210"}
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

def test_create_user(client):
    res = client.post("/users", json={"email": "hello@gmail.com",
                                      "password": "khang1210"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201

def test_user_login(test_user, client):
    res = client.post("/login", data = {"username": test_user["email"],
                                        "password": test_user["password"]})
    
    assert res.status_code == 200