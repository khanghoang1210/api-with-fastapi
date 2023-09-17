from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="postgres", user="postgres",
                                password="khang12102003", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as exp:
        print("Connecting to database failed")
        print("Error:", str(exp))
        time.sleep(2)

my_posts = [{"id": 111111}, {"id": 123123123}]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
        
def find_post_id(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "This is root"}

@app.get("/posts")
def get_posts():
    cursor.execute("""select * from posts""")
    posts = cursor.fetchall()
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""insert into posts (title, content, published) values(%s, %s, %s) 
                                                                        returning *""",
                   (post.title, post.content, post.published))
    new_posts = cursor.fetchall()
    conn.commit()
    return {"data": new_posts}


@app.get("/posts/{id}")
def get_post(id: str):
    cursor.execute("""select * from posts where id = %s""",(id))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""delete from posts where id = %s returning *""",
                   (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with {id} does not exist")
    return {"data": updated_post}