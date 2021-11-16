from pydantic import BaseModel

# SCHEMA/PYDANTIC MODEL - defines the structure of the request/response
class Post(BaseModel):
    title:str
    content:str
    published:bool=True

class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True

# Below class extends PostBase class in its entirety
class PostCreate(PostBase):
    pass

# Below class extends Postbase and allows user to only update the published field
class PostUpdate(PostBase):
    published:bool

