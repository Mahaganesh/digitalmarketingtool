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


@router.post('/create-organisation')
def create_organisation(organisationname: str, db: Session = Depends(get_db),file: UploadFile = File(...), current_user: models.User = Depends(get_current_user)):
    print(current_user.uuid)
    if str(file.filename) == "":
        return {'details': 'Please add image'}
    if str(organisationname) == "":
        return {'details': 'Please add projectname'}
    else:
        projectexist = db.query(models.organisation).filter(models.organisation.organisation_name == organisationname, models.organisation.created_by==current_user.uuid).all()
        # try:
        if projectexist:
            return {'details' : 'Organisation name already exist'}
        else:
            # image_url = media(current_user.uuid, organisationname, organisationname,file)
            image_url = "https://cdn.pixabay.com/photo/2021/08/25/20/42/field-6574455__340.jpg"
            db_project = models.organisation(organisation_name=organisationname, created_by=current_user.uuid, logo_url = image_url)
            db.add(db_project)
            db.commit()
            db.refresh(db_project)
            return {'details' : 'Organisation created successfully'}
        # except:
        #     return {'details' : 'Something went wrong'}

@router.get('/organisaton-all/')
def get_organisation(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    organisation_all = db.query(models.organisation).filter(models.organisation.created_by == user_id).all()
    return organisation_all


@router.get('/user-organisation-all/')
def get_organisation_all(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    organisation_all = db.query(models.organisation).filter(models.organisation.created_by == user_id, models.organisation.is_deleted == False).all()
    return organisation_all

@router.get('/user-organisation-details/{organisation_uuid}')
def organisation_details(organisation_uuid: str ,current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    organisation_all = db.query(models.organisation).filter(models.organisation.created_by == user_id, models.organisation.uuid ==  organisation_uuid, models.organisation.is_deleted == False).all()
    return organisation_all

@router.get('/user-organisation-brand/{organisationuuid}')
def get_brand_by_organisation(organisationuuid: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    data = []
    organisation_all = db.query(models.organisation).filter(models.organisation.created_by == user_id, models.organisation.uuid ==  organisationuuid, models.organisation.is_deleted == False).all()
    for organisation in organisation_all:
        brand_all = db.query(models.brand).filter(models.brand.organisation_uuid == organisation.uuid, models.brand.created_by == user_id, models.brand.is_deleted == False).all()
        organisation.brands = brand_all
        data.append(organisation)
    return data

@router.get('/user-organisation-all-brand/')
def get_all_brand_by_organisation(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    data = []
    organisation_all = db.query(models.organisation).filter(models.organisation.created_by == user_id, models.organisation.is_deleted == False).all()
    for organisation in organisation_all:
        brand_all = db.query(models.brand).filter(models.brand.organisation_uuid == organisation.uuid, models.brand.created_by == user_id, models.brand.is_deleted == False).all()
        organisation.brands = brand_all
        data.append(organisation)
    return data


@router.patch('/project-patch/{organisation_uuid}')
def update_organisation(organisation_uuid: str, data : schemas.Pojectupdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    organisation = db.query(models.organisation).filter(models.organisation.created_by == user_id, models.organisation.uuid ==  organisation_uuid, models.organisation.is_deleted == False).all()
    data.updated_by = user_id
    if not organisation:
        return HTTPException(status_code=400, detail='Invalid organisation')
    db_update = db.query(models.organisation).filter(models.organisation.uuid == organisation_uuid).update(vars(data))
    db.commit()
    return HTTPException(status_code=200, detail='Project updated successfully')
    

# @router.patch('/organisation-patch2/{organisation_uuid}')
# def update_organisation(organisation_uuid: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
#     user_id = current_user.uuid
#     organisation = db.query(models.organisation).filter(models.organisation.created_by == user_id, models.organisation.uuid ==  organisation_uuid, models.organisation.is_deleted == False).all()
#     updated_by = user_id
#     if not organisation:
#         return HTTPException(status_code=400, detail='Invalid organisation')
#     db_update = db.query(models.organisation).filter(models.organisation.uuid == organisation_uuid).update(vars(updated_by))
#     db.commit()
#     return HTTPException(status_code=200, detail='Project updated successfully')


@router.delete('/organisation-delete/{organisation_uuid}')
def delete_organisation(organisation_uuid: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    user = db.query(models.User).filter(models.User.uuid == user_id).first()
    if user:
        db_organisation = db.query(models.organisation).filter(models.organisation.uuid == organisation_uuid).first()
        if db_organisation:
            db_organisation.is_deleted = True
            db_organisation.updated_by = user_id
            db.commit()
            return {'success': True}
        else:
            return {'detail': 'Organisation does not exist'}

    else:
        return {'Failed': 'Something went wrong'}
    



