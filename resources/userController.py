import re

from jose import JWTError, jwt


from fastapi import Depends, APIRouter, HTTPException, Request, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from config.base_config import BaseConfig
from resources.authController import get_current_user
from config.dev_config import Configuration

from models import  models, get_db
from models.schemas import schemas


from email_validator import validate_email
from resources.utils import email_sender, email_sender1

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/oauth/authorize")


@router.post("/users")
def create_user(user : schemas.RegisterUser, db: Session = Depends(get_db)):
    user.username = user.username.lower()
    user.email = user.email.lower()
    db_user = db.query(models.User).filter(or_(models.User.username == user.username, models.User.email == user.email)).first()
    if db_user:
        error_msg = "Username / Email already exist"
        raise HTTPException(status_code=400, detail=error_msg)    
    try:
        validate_email(user.email)
    except:
        raise HTTPException(status_code=400, detail='Please enter a valid E-Mail')
    if len(user.password) < 8:
        error_msg = "Password is less than 8 characters"
        raise HTTPException(status_code=400, detail=error_msg)
    db_user = models.User(firstname=user.fname,lastname=user.lname ,username=user.username, email = user.email)
    db_user.hash_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    del db_user.password
    try:
        email_response = email_sender1(user.email, 'Verification Email')
        if email_response:
            return db_user
        else:
            raise HTTPException(status_code=400, detail="Something went wrong")
    except:
        return db_user


@router.get("/user/{uuid}")
def get_user( uuid: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.uuid == uuid).first()
    del db_user.password
    return db_user



@router.get("/all/users")
def get_value(db: Session = Depends(get_db)):
    db_user = db.query(models.User).all()
    return db_user

