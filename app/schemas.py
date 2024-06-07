# app/schemas.py

from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Literal, Optional


# ************ USERS *************
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ************ POSTS *************
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


# ************ VOTES *************


class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]
