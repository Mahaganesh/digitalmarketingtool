from fastapi.openapi.models import Schema
from datetime import datetime, timedelta
from typing import Optional

from jose.constants import Algorithms
from pydantic.typing import update_field_forward_refs
from sqlalchemy.sql.elements import or_
from sqlalchemy.sql.expression import false, null
from sqlalchemy.sql.sqltypes import NullType
from starlette.responses import HTMLResponse
from models.schemas import schemas
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode, user
from config.base_config import BaseConfig
from config.dev_config import Configuration
from models import models, get_db
from passlib.context import CryptContext
import os
from resources.authController import get_current_user
import shutil

from resources.utils import media


router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/oauth/authorize")


@router.post('/create-brand/')
def create_brand(organisationuuid: str, brandname: str, db: Session = Depends(get_db),file: UploadFile = File(...), current_user: models.User = Depends(get_current_user)):
    print(current_user.uuid)
    if str(file.filename) == "":
        return {'details': 'Please add image'}
    if str(brandname) == "":
        return {'details': 'Please add projectname'}
    else:
        projectexist = db.query(models.brand).filter(models.brand.brand_name == brandname, models.brand.created_by==current_user.uuid).all()
        try:
            if projectexist:
                return {'details' : 'Brand name already exist'}
            else:
                # image_url = media(current_user.uuid, brandname, brandname,file)
                image_url = "https://cdn.pixabay.com/photo/2021/08/25/20/42/field-6574455__340.jpg"
                db_project = models.brand(brand_name=brandname, organisation_uuid=organisationuuid, created_by=current_user.uuid, logo_url = image_url)
                db.add(db_project)
                db.commit()
                db.refresh(db_project)
                return {'details' : 'brand created successfully'}
        except: 
            return {'details' : 'Something went wrong'}

@router.get('/brand-all/')
def get_brand(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    brand_all = db.query(models.brand).filter(models.brand.created_by == user_id).all()
    return brand_all


@router.get('/user-brand-all/')
def get_brand_all(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    brand_all = db.query(models.brand).filter(models.brand.created_by == user_id, models.brand.is_deleted == False).all()
    return brand_all

@router.get('/user--brand/{organisationuuid}')
def get_by_organisation(organisationuuid: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    brand_all = db.query(models.brand).filter(models.brand.organisation_uuid == organisationuuid, models.brand.created_by == user_id, models.brand.is_deleted == False).all()
    return brand_all

@router.get('/user-brand-details/{brand_uuid}')
def brand_details(brand_uuid: str ,current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    brand_all = db.query(models.brand).filter(models.brand.created_by == user_id, models.brand.uuid ==  brand_uuid, models.brand.is_deleted == False).all()
    return brand_all

@router.patch('/brand-patch/{brand_uuid}')
def update_brand(brand_uuid: str, data : schemas.Pojectupdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    brand = db.query(models.brand).filter(models.brand.created_by == user_id, models.brand.uuid ==  brand_uuid, models.brand.is_deleted == False).all()
    data.updated_by = user_id
    if not brand:
        return HTTPException(status_code=400, detail='Invalid organisation')
    db_update = db.query(models.brand).filter(models.brand.uuid == brand_uuid).update(vars(data))
    db.commit()
    return HTTPException(status_code=200, detail='Project updated successfully')



@router.patch('/brand-patch2/{brand_uuid}')
def update_brand(brand_uuid: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    brand = db.query(models.brand).filter(models.brand.created_by == user_id, models.brand.uuid ==  brand_uuid, models.brand.is_deleted == False).all()
    updated_by = user_id
    if not brand:
        return HTTPException(status_code=400, detail='Invalid organisation')
    db_update = db.query(models.brand).filter(models.brand.uuid == brand_uuid).update(vars(updated_by))
    db.commit()
    return HTTPException(status_code=200, detail='Brand updated successfully')


@router.delete('/brand-delete/{brand_uuid}')
def delete_brand(brand_uuid: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    user = db.query(models.User).filter(models.User.uuid == user_id).first()
    if user:
        db_brand = db.query(models.brand).filter(models.brand.uuid == brand_uuid).first()
        if db_brand:
            db_brand.is_deleted = True
            db_brand.updated_by = user_id
            db.commit()
            return {'success': True}
        else:
            return {'detail': 'Brand does not exist'}

    else:
        return {'Failed': 'Something went wrong'}
    