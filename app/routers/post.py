from fastapi import FastAPI,Response, status, HTTPException,Depends,APIRouter
from .. import models,schemas,oauth2
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import  get_db

router = APIRouter(
     prefix="/posts",
     tags=["Posts"]
)


# GET ALL POSTS
@router.get("/")
def get_posts(db:Session = Depends(get_db),
current_user: int = Depends(oauth2.get_current_user),
response_model=List[schemas.PostOut],
limit:int = 10,skip: int=0,
search:Optional[str]=""
):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # 
    return posts
    

# @router.post("/posts")
# def create_post(payload:dict=Body(...)):
#     print(payload)
#       my_posts.append(payload)
#     return {
#         "new post":f"Title: {payload['title']} . Content: {payload['content']}"
#     }

# CREATE A POST
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db: Session = Depends(get_db),
  current_user: int = Depends(oauth2.get_current_user)):
    post = models.Post(owner_id=current_user.id, **post.dict())
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
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id==id).first()
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} not found.")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are not authorized to perform this operation.")
    return post
    


# DELETE A POST
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db),
current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id= %s RETURNING * """,(str(id),))
    # post=cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} does not exist.")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform this operation")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE A POST
@router.patch("/{id}",response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.PostCreate,
 db: Session = Depends(get_db),
 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id),))
    # post=cursor.fetchone()
    # conn.commit()
    post_query= db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} does not exist.")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform this operation")

    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
