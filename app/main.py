from fastapi import FastAPI,Response, status, HTTPException,Depends
from pydantic import BaseModel
from random import randrange
from typing import Optional, List

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import engine, get_db
from .routers import post,user,auth


models.Base.metadata.create_all(bind=engine)

app =FastAPI()

# DATABASE CONNECTION
while True:
    try:
        conn=psycopg2.connect(host="localhost",database="fastapi",user="postgres",
        password="Mahachula123#!",cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connected succesfully.")
        break
    except Exception as error:
        print("Connecting to database failed.")
        print("Error",error)
        time.sleep(2)

# FIND ARRAY INDEX OF A SINGLE POST
def find_index_post(id):
    for index,post in enumerate(my_posts):
        if post['id']==id:
            return index

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

#  HOME PAGE
@app.get("/")
async def root():
    return {
        "message":"Hello World."
    }


