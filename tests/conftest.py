from fastapi.testclient import TestClient
from app.main import app

from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models
import pytest




SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base.metadata.create_all(bind=engine)



@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
 
@pytest.fixture
def test_user(client):
    user_data = {"email":"khang@gmail.com",
                 "password": "khang1210"}
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user 

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session):
    posts_data = [{
        "title": "first title",
        "content": " first content",
        "owner_id": test_user['id']
    },
    {
        "title": "second title",
        "content": "second content",
        "owner_id": test_user["id"]
    },
    {
        "title": "third title",
        "content": "third content",
        "owner_id": test_user["id"]
    }]

    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()

    return posts