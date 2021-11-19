from fastapi import FastAPI,Response, status, HTTPException,Depends,APIRouter
from .. import models,schemas
from typing import List
from sqlalchemy.orm import Session
from ..database import  get_db

router = APIRouter()


# GET ALL POSTS
@router.get("/posts")
def get_posts(db:Session = Depends(get_db),response_model=List[schemas.Post]):
    posts = db.query(models.Post).all()
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    return posts
    

# @router.post("/posts")
# def create_post(payload:dict=Body(...)):
#     print(payload)
#       my_posts.append(payload)
#     return {
#         "new post":f"Title: {payload['title']} . Content: {payload['content']}"
#     }

# CREATE A POST
@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
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
@router.get("/posts/{id}",response_model=schemas.Post)
def get_post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} not found.")
    return post
    


# DELETE A POST
@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
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
@router.put("/posts/{id}",response_model=schemas.Post)
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
