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


@router.get('/get')
def get(current_user: models.User = Depends(get_current_user)):
    return current_user.uuid

@router.post('/create-project/')
def create_project(projectname: str, db: Session = Depends(get_db),file: UploadFile = File(...), current_user: models.User = Depends(get_current_user)):
    print(current_user.uuid)
    if str(file.filename) == "":
        return {'details': 'Please add image'}
    if str(projectname) == "":
        return {'details': 'Please add projectname'}
    else:
        projectexist = db.query(models.project).filter(models.project.project_name == projectname, models.project.created_by==current_user.uuid).all()
        try:
            if projectexist:
                return {'details' : 'Project name already exist'}
            else:
                # image_url = media(current_user.uuid,projectname,projectname,file)
                image_url = "https://cdn.pixabay.com/photo/2021/08/25/20/42/field-6574455__340.jpg"
                db_project = models.project(project_name=projectname,created_by=current_user.uuid, logo = image_url)
                db.add(db_project)
                db.commit()
                db.refresh(db_project)
                return {'details' : 'Created Project successfully'}
        except:
            return {'details' : 'Something went wrong'}
   
 
        
@router.get('/projects-all/')
def get_project(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    project_all = db.query(models.project).filter(models.project.created_by == user_id).all()
    return project_all

@router.get('/user-projects-all/')
def get_project(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    project_all = db.query(models.project).filter(models.project.created_by == user_id, models.project.is_deleted == False).all()
    return project_all

@router.get('/user-project-details/{project_uuid}')
def project_details(project_uuid: str ,current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    project_all = db.query(models.project).filter(models.project.created_by == user_id, models.project.uuid ==  project_uuid, models.project.is_deleted == False).all()
    return project_all

@router.patch('/project-patch/{project_uuid}')
def update_project(project_uuid: str, data : schemas.Pojectupdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    project = db.query(models.project).filter(models.project.created_by == user_id, models.project.uuid ==  project_uuid, models.project.is_deleted == False).all()
    data.updated_by = user_id
    if not project:
        return HTTPException(status_code=400, detail='Invalid project')
    db_update = db.query(models.project).filter(models.project.uuid == project_uuid).update(vars(data))
    db.commit()
    return HTTPException(status_code=200, detail='Project updated successfully')



@router.patch('/project-patch2/{project_uuid}')
def update_project(project_uuid: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    project = db.query(models.project).filter(models.project.created_by == user_id, models.project.uuid ==  project_uuid, models.project.is_deleted == False).all()
    updated_by = user_id
    if not project:
        return HTTPException(status_code=400, detail='Invalid project')
    db_update = db.query(models.project).filter(models.project.uuid == project_uuid).update(vars(updated_by))
    db.commit()
    return HTTPException(status_code=200, detail='Project updated successfully')


@router.delete('/project-delete/{project_uuid}')
def delete_project(project_uuid: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    user = db.query(models.User).filter(models.User.uuid == user_id).first()
    if user:
        db_project = db.query(models.project).filter(models.project.uuid == project_uuid).first()
        if db_project:
            db_project.is_deleted = True
            db_project.updated_by = user_id
            db.commit()
            return {'success': True}
        else:
            return {'detail': 'Project does not exist'}
    else:
        return {'Failed': 'Something went wrong'}
    