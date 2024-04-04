# import uuid

from os import name
from sqlalchemy import orm
from sqlalchemy.sql.sqltypes import JSON
from models.models import Base, User
from typing import List , Optional
# from uuid import UUID
from pydantic import BaseModel
import datetime
from fastapi import FastAPI, File, UploadFile


class RegisterUser(BaseModel):
    fname: str
    lname: str
    username: str
    password : str
    email: str

    class Config:
        orm_mode = True


class ResetPassword(BaseModel):

    New_password: str
    confirm_password: str

    class Config:
        orm_mode = True


class Project(BaseModel):
    
    project_name: str
    user_id: str



# Facebook
class FBpages(BaseModel):
    
    facebook_page_id: int

    class Config:
        orm_mode = True

class FBlikes(BaseModel):

    facebook_page_id: int



class FBmedia(BaseModel):

    facebook_media_url: str



class IGPage(BaseModel):

    facebook_page_id: int


class IGSearch(BaseModel):
    
    username : str


class IGHashtag(BaseModel):

    hashtag : str

class FBPublic(BaseModel):

    accesstoken : str


class IDauth(BaseModel):
    authtoken : str

class INaccess_token(BaseModel):
    accesstoken : str


class Pinauth(BaseModel):

    auth_code: str

class Pinaccess(BaseModel):

    access_token: str

class Pinboard(BaseModel):

    board_id : str

class Pinpin(BaseModel):

    pin_id : str


class Pojectupdate(BaseModel):

    project_name: str
    updated_by : str
    class Config:
        orm_mode = True

class Fbprofiles(BaseModel):
    fb_page_id : str
    fb_page_name : str

class SMprofiles(BaseModel):

    platform : str
    project_uuid : str
    page_id : str
    access_token : str
