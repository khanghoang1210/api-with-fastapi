from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "This is root"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}

@app.post("/createposts")
def create_posts(new_post: Post):
    print(new_post)
    return {"data": "successfully"}