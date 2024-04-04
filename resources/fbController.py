from re import I, S
import time, calendar

from resources.utils import page_access_token, public_page_access_token, media
from fastapi import APIRouter, Depends, HTTPException, routing, status, Request, Header, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
import requests
from sqlalchemy.orm import immediateload
from sqlalchemy.sql.sqltypes import JSON
from starlette import responses
from starlette.types import Message
from config.base_config import BaseConfig
from models.schemas import schemas
from sqlalchemy.orm import Session
from resources.authController import get_current_user

import json
import shutil
from datetime import date, datetime
from models import models, get_db



router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/oauth/authorize")

# @router.get('/facebook/me')
# def facebook_user(request: Request):    
#     data =  requests.get('https://graph.facebook.com/v12.0/me?fields=id,name&access_token={}'.format(BaseConfig.FB_token)).json()
#     if data:
#         name = data['name']
#         id = data['id']
#         return {'account_name': name, 'account_id':id}
#     else:
#         raise HTTPException(status_code=400, detail="Something went wrong")

# @router.post('/facebook/users')
# def facebook_pages(request:Request, Page_id : schemas.FBpages):
#     data =  requests.get('https://graph.facebook.com/v12.0/{}/accounts?limit=100&access_token={}'.format(Page_id.facebook_page_id, BaseConfig.FB_token)).json()
#     response = []
#     for x in data['data']:
#         page = {
#             'name': x['name'],
#             'id': x['id']
#         }
#         response.append(page)
#     raise HTTPException(status_code=200, detail=response)
    


# @router.post('/facebook/post_details')
# def post_details(request: Request, fb_likes : schemas.FBlikes):
#     data = page_access_token(fb_likes.facebook_page_id)
#     if data:
#         response = []
#         for x in data['data']:
#             if 'message' in x:
#                 x['message']
#             else:
#                 x['message'] = 'No content'
#             image_id = x['id']
#             image_likes = x['likes']['summary']['total_count']
#             post_link = "https://www.facebook.com/{}".format(image_id)
#             comment_response = []
#             if 'comments' in x:
#                 for c in x['comments']['data']:
#                     comments = { 
#                         'comment_by' : 'Facebbok Does not Provide',
#                         'comments': c['message'] 
#                         }   
#                     comment_response.append(comments)
#             else:
#                 comment_response = {
#                     'message' : 'No comments found'
#                 }
#             if 'full_picture' in x:
#                 x['full_picture']
#             else:
#                 x['full_picture'] = 'No Url'
#             Post = {
#                 'post_id' : image_id,
#                 'content' : x['message'],
#                 'post_image_url' : x['full_picture'],
#                 'post_likes' : image_likes,
#                 'post_link' : post_link,
#                 'comments' : comment_response
#             }
#             response.append(Post)
#     raise HTTPException(status_code=200, detail=response)



@router.post('/facebook/pages-publics-user')
def facebook_pages_public_user(access: schemas.FBPublic):
    data =  requests.get('https://graph.facebook.com/v12.0/me?fields=id,name&access_token={}'.format(access.accesstoken)).json()
    if data:
        name = data['name']
        id = data['id']
        url = "https://graph.facebook.com/v12.0/me?fields=accounts{id,access_token,name}&limit=9"

        payload={}
        headers = {
        'Authorization': 'Bearer {}'.format(access.accesstoken),
        'Cookie': 'fr=1LmLOnjYt3rgeKdsh..BhPwvK.de.AAA.0.0.BhPwvK.AWUix2Z3vqw; sb=ygs_YV2GbnbI2wjJZ2NROlTu'
        }

        data1 = requests.request("GET", url, headers=headers, data=payload).json()
        data2 = data1['accounts']
        response = []
        for x in data2['data']:
            page = {
                'name': x['name'],
                'id': x['id'],
                'access_token' : x['access_token']
            }
            response.append(page)
        raise HTTPException(status_code=200, detail=response)
    else:
        raise HTTPException(status_code=400, detail="Something went wrong")
    


@router.post('/facebook/public-me')
def facebook_user(request: Request, access: schemas.FBPublic):    
    data =  requests.get('https://graph.facebook.com/v12.0/me?fields=id,name&access_token={}'.format(access.accesstoken)).json()
    if data:
        name = data['name']
        id = data['id']
        return {'account_name': name, 'account_id':id}
    else:
        raise HTTPException(status_code=400, detail="Something went wrong")
    

@router.post('/facebook/public-page')
def facebook_pages(request:Request, Page_id : schemas.FBpages, access: schemas.FBPublic):
    data =  requests.get('https://graph.facebook.com/v12.0/{}/accounts?limit=100&access_token={}'.format(Page_id.facebook_page_id, access.accesstoken)).json()
    response = []
    for x in data['data']:
        page = {
            'name': x['name'],
            'id': x['id'],
            
        }
        response.append(page)
    raise HTTPException(status_code=200, detail=response)


@router.post('/facebook/public-page-me')
def facebook_page_me(request:Request, Page_id : schemas.FBpages, access: schemas.FBPublic):
    page_access_token = public_page_access_token(Page_id.facebook_page_id, access.accesstoken)
    url = "https://graph.facebook.com/v12.0/{}?fields=id,name,picture,cover,access_token".format(Page_id.facebook_page_id)
    payload={}
    headers = {
    'Authorization': 'Bearer {}'.format(page_access_token),
    'Cookie': 'fr=1LmLOnjYt3rgeKdsh..BhPwvK.de.AAA.0.0.BhPwvK.AWUix2Z3vqw; sb=ygs_YV2GbnbI2wjJZ2NROlTu'
    }
    response = requests.get(url, headers=headers, data=payload).json()
    id = response['id']
    name = response['name']
    picture = response['picture']['data']['url']
    cover = response['cover']['source']
    data = {
        'page_id'              : id,
        'page_name'            : name,
        'page_profile_picture' : picture,
        'page_cover_picture'   : cover
    }
    return data

@router.post('/facebook/public-page-post')
def facebook_page_post(request:Request,message : str, Page_id : schemas.FBpages, access: schemas.FBPublic):
    page_access_token = public_page_access_token(Page_id.facebook_page_id, access.accesstoken)
    url = "https://graph.facebook.com/v12.0/105918195193738/feed?message={}&link=https://developers.facebook.com/docs/workplace/custom-integrations/apps".format(message)
    payload={}
    headers = {
    'Authorization': 'Bearer {}'.format(page_access_token),
    'Cookie': 'fr=1LmLOnjYt3rgeKdsh..BhPwvK.de.AAA.0.0.BhPwvK.AWUix2Z3vqw; sb=ygs_YV2GbnbI2wjJZ2NROlTu'
    }
    response = requests.post(url, headers=headers, data=payload).json()

    return response

@router.post('/facebook/public-page-post-image')
def facebook_page_post_image(projectuuid:str ,message: str,Page_id : str, access: str, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    page_access_token = public_page_access_token(Page_id, access)
    platform_name = "Facebook"
    image_url = media(current_user.uuid,projectuuid,platform_name,file)
    url = "https://graph.facebook.com/v12.0/{}/photos?url={}&message={}&access_token={}".format(Page_id, image_url, message, page_access_token)
    
    response = requests.post(url)
    if response.status_code == 200:
        status_report = 'Success'
    else:
        status_report = 'Failed'
    post_details = models.Post(created_by=current_user.uuid, project_uuid=projectuuid, platform=platform_name ,description=message,upload_url=image_url,status=status_report)
    attachment_details = models.attachments(created_by=current_user.uuid, project_uuid=projectuuid,url=image_url)
    db.add(post_details)
    db.add(attachment_details)
    db.commit()
    db.refresh(post_details)
    db.refresh(attachment_details)
    return HTTPException(status_code=200, detail='Post Created Successfully')

@router.post('/facebook/public-page-insights')
def facebook_page_insights(Page_id : schemas.FBpages, access: schemas.FBPublic, start_date: datetime = datetime.today(), end_date: datetime = datetime.today()):
    page_access_token = public_page_access_token(Page_id.facebook_page_id, access.accesstoken)
    data = requests.get("https://graph.facebook.com/v12.0/{}/insights?metric=page_views_logout,page_views_logged_in_total,page_views_total,page_fans,page_fans_gender_age,page_fan_removes_unique&period=day&since={}&until={}&access_token={}".format(Page_id.facebook_page_id,start_date,end_date,page_access_token)).json()
    return data


@router.get('/facebook/refresh-token')
def facebook_refresh_token(access_token : str):
    url = "https://graph.facebook.com/v12.0/oauth/access_token?grant_type=fb_exchange_token&client_id=1639989929665722&client_secret=d705fceb8c30c1aac05926b3f8f4a152&fb_exchange_token={}".format(access_token)

    payload={}
    headers = {
    'Cookie': 'fr=1LmLOnjYt3rgeKdsh..BhPwvK.de.AAA.0.0.BhPwvK.AWUix2Z3vqw; sb=ygs_YV2GbnbI2wjJZ2NROlTu'
    }

    response = requests.get(url, headers=headers, data=payload).json()
    expires_in = calendar.timegm(time.gmtime()) + 5184000
    data = {
        'access_token': response['access_token'],
        'token_type' : 'Bearer',
        'expires_in' : expires_in
    }
    return data
    
