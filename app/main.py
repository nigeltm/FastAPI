from fastapi import FastAPI,Response, status, HTTPException
from fastapi.params import Body,Optional
from pydantic import BaseModel
from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor
import time


app =FastAPI()


class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    rating: Optional[int]=None

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
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    print("=====")
    print(posts)
    print("++++")
    return {
        "data":posts
    }

# @app.post("/posts")
# def create_post(payload:dict=Body(...)):
#     print(payload)
#       my_posts.append(payload)
#     return {
#         "new post":f"Title: {payload['title']} . Content: {payload['content']}"
#     }

# CREATE A POST
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    cursor.execute(""" INSERT INTO posts(title,content,published)
    VALUES(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    post=cursor.fetchone()
    conn.commit()
    return {
        "data":post
    }


#  GET A POST
@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} not found.")
    return {
        "data":post
    }


# DELETE A POST
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute(""" DELETE FROM posts WHERE id= %s RETURNING * """,(str(id),))
    post=cursor.fetchone()
    conn.commit()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} does not exist.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE A POST
@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    cursor.execute(""" UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id),))
    post=cursor.fetchone()
    conn.commit()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} does not exist.")
    return {"data":post}