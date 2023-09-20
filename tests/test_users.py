from app import schemas
from .database import client, session


def test_root(client):
    res = client.get("/")
    print(res.json())
    assert res.json().get("message") == "Hello world"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users", json={"email": "hello@gmail.com",
                                      "password": "khang1210"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201