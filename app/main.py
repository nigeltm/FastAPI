from fastapi import FastAPI,Response, status, HTTPException,Depends
from pydantic import BaseModel
from random import randrange
from typing import Optional, List

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas
from .database import engine, get_db

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


#  HOME PAGE
@app.get("/")
async def root():
    return {
        "message":"Hello World."
    }


# GET ALL POSTS
@app.get("/posts")
def get_posts(db:Session = Depends(get_db),response_model=List[schemas.Post]):
    posts = db.query(models.Post).all()
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    return posts
    

# @app.post("/posts")
# def create_post(payload:dict=Body(...)):
#     print(payload)
#       my_posts.append(payload)
#     return {
#         "new post":f"Title: {payload['title']} . Content: {payload['content']}"
#     }

# CREATE A POST
@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db: Session = Depends(get_db)):

    post = models.Post(**post.dict())
    db.add(post)
    db.commit()
    # TO RETURN NEWLY CREATED POST IN THE ENDPOINT
    db.refresh(post) 
    # cursor.execute(""" INSERT INTO posts(title,content,published)
    # VALUES(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # post=cursor.fetchone()
    # conn.commit()

    return post
    


#  GET A POST
@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} not found.")
    return post
    


# DELETE A POST
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id= %s RETURNING * """,(str(id),))
    # post=cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id==id)
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} does not exist.")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE A POST
@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id),))
    # post=cursor.fetchone()
    # conn.commit()
    post_query= db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} does not exist.")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()