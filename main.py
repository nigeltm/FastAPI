from fastapi import FastAPI
from fastapi.params import Body,Optional
from pydantic import BaseModel
from random import randrange

app =FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    rating: Optional[int]=None

my_posts=[{"title":"Post 1 title","content":"Post 1 content.","id":1},

]

@app.get("/")
async def root():
    return {
        "message":"Hello World."
    }

@app.get("/posts")
def get_posts():
    return {
        "data":my_posts
    }

# @app.post("/posts")
# def create_post(payload:dict=Body(...)):
#     print(payload)
#     return {
#         "new post":f"Title: {payload['title']} . Content: {payload['content']}"
#     }

@app.post("/posts")
def create_post(post:Post):
    post_dict=post.dict()
    post_dict['id']=randrange(0,1000000)
    my_posts.append(post_dict)
    return {
        "data":post_dict
    }

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p

@app.get("/posts/{id}")
def get_post(id:int):
    post=find_post(id)
    return {
        "data":post
    }

@app.put("/posts/{id}")
def update_post():
    return{"data":"Post updated successfully."}

@app.delete("/posts/{id}")
def delete_post():
    return {"data":"Post deleted successfully."}

