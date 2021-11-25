from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user,auth,vote
from .config import settings

models.Base.metadata.create_all(bind=engine)

app =FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#  HOME PAGE
# @app.get("/")
# async def root():
#     return {
#         "message":"Hello World."
#     }



# FIND ARRAY INDEX OF A SINGLE POST
# def find_index_post(id):
#     for index,post in enumerate(my_posts):
#         if post['id']==id:
#             return index