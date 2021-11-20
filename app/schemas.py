from pydantic import BaseModel,EmailStr
from datetime import datetime

# SCHEMA/PYDANTIC MODEL - defines the structure of the request/response
class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True

# Below class extends PostBase class in its entirety
class PostCreate(PostBase):
    pass

#Pydantic model for the response, explicitly defines fileds to be send back to the user
class Post(PostBase):
    id:int
    created_at:datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email : EmailStr
    password: str

class UserOut(BaseModel):
    id:int
    email: EmailStr
    created_at:datetime

    class Config:
        orm_mode=True

class UserLogin(BaseModel):
    email:EmailStr
    password:str

