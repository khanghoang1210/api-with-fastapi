from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth
models.Base.metadata.create_all(bind=engine)

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

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "This is root"}



