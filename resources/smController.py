from fastapi.openapi.models import Schema
from datetime import datetime, timedelta
from typing import Optional

from jose.constants import Algorithms
from sqlalchemy.sql.elements import or_
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.operators import exists
from models.schemas import schemas
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode, user
from config.base_config import BaseConfig
from config.dev_config import Configuration
from models import models, get_db

import os
import requests
from resources.authController import get_current_user
import shutil

from resources.utils import SM_FB_profile_pic, SM_IG_profile_pic, media

router = APIRouter()



@router.post('/create-social-media/')
def create_social_media(smplatform : schemas.SMprofiles, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    user_id = current_user.uuid
    sm_exist = db.query(models.User_social_media).filter(
            models.User_social_media.created_by == user_id,
            models.User_social_media.project_uuid ==  smplatform.project_uuid,
            models.User_social_media.page_id == smplatform.page_id,
            models.User_social_media.sm_platform == smplatform.platform).all()
    if not sm_exist:
        if smplatform.platform == "facebook":
            data = SM_FB_profile_pic(smplatform.access_token)
            db_social = models.User_social_media(
                created_by = user_id, 
                project_uuid = smplatform.project_uuid, 
                page_id = smplatform.page_id, 
                sm_access_token = smplatform.access_token, 
                sm_platform = smplatform.platform,
                profile_pic = data['profile'],
                cover_pic = data['cover'],
                username = data['name'])
            db.add(db_social)
            db.commit()
            db.refresh(db_social)
            return HTTPException(status_code=200, detail='Facebook Added successfully')
        elif smplatform.platform == "instagram":
            data = SM_IG_profile_pic(smplatform.access_token, smplatform.page_id)
            db_social = models.User_social_media(
                    created_by = user_id, 
                    project_uuid = smplatform.project_uuid, 
                    page_id = data['ig_id'], 
                    sm_access_token = smplatform.access_token, 
                    sm_platform = smplatform.platform,
                    profile_pic = data['profile'],
                    username = data['name'])
            db.add(db_social)
            db.commit()
            db.refresh(db_social)
            return HTTPException(status_code=200, detail='Instagram Added successfully')
        else:
            return HTTPException(status_code=400, detail='Something went wrong')
    else:
        return HTTPException(status_code=200, detail='Social Profile Already Exist')


@router.get('/user-project-details/')
def get_social_media(project_id: str,  db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    media = db.query(models.User_social_media).filter(models.User_social_media.project_uuid == project_id, models.User_social_media.created_by == current_user.uuid, models.User_social_media.is_deleted == False).all()
    return media

@router.delete('/project-delete/{projectuuid}/{sm_uuid}')
def delete_project(projectuuid: str, sm_uuid:str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.uuid
    user = db.query(models.User).filter(models.User.uuid == user_id).first()
    if user:
        db_project = db.query(models.project).filter(models.User_social_media.uuid == sm_uuid, models.User_social_media.project_uuid==projectuuid).first()
        if db_project:
            db_project.is_deleted = True
            db_project.updated_by = user_id
            db.commit()
            return {'success': True}
        else:
            return {'detail': 'Project does not exist'}

    else:
        return {'Failed': 'Something went wrong'}
    

