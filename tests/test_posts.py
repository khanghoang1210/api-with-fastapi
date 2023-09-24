
import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def  validate(post):
        return schemas.PostOut(**post)
    
    posts_map = map(validate, res.json())
    posts = list(posts_map)
    
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unathorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    assert res.status_code == 401

def test_unathorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/1111")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert res.status_code == 200

@pytest.mark.parametrize("title, content", [
    ("some thing 1", "some thing 1"),
    ("some thing 2", "some thing 2"),
    ("some thing 3", "some thing 3")
])
def test_create_post(authorized_client, test_user, test_posts, title, content):
    res = authorized_client.post("/posts/", json={"title": title, "content": content})

    created_post = schemas.Post(**res.json())
    
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.owner_id == test_user['id']

def test_unathorized_user_create_post(client, test_posts, test_user):
    res = client.post("/posts/", json={"title": "something", "content": "something"})

    assert res.status_code == 401