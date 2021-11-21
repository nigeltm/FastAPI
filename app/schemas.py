from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

# SCHEMA/PYDANTIC MODEL - defines the structure of the request/response
class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True

# Below class extends PostBase class in its entirety
class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id:int
    email: EmailStr
    created_at:datetime

    class Config:
        orm_mode=True

#Pydantic model for the response, explicitly defines fields to be send back to the user
class Post(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner:int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email : EmailStr
    password: str


class UserLogin(BaseModel):
    email:EmailStr
    password:str

# DEFINE SCHEMA FOR ACCESS TOKEN AND TOKEN TYPE
class Token(BaseModel):
    token:str
    token_type:str

# SCHEMA FOR TOKEN DATA
class TokenData(BaseModel):
    id: Optional[str] =  None