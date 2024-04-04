from datetime import date, datetime
from re import I, S
import re

from resources.utils import IG_page_access_token, IG_search_account, page_access_token, extract_hashtags, hashtag_validation, IG_page_access_token_and_Id, IG_public_page_access_token_and_Id, media
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
import requests
from sqlalchemy.orm import immediateload
from sqlalchemy.sql.sqltypes import JSON, Date
from starlette import responses
from starlette.types import Message
from config.base_config import BaseConfig
from models.schemas import schemas
from pydantic import BaseModel, Field
import json
from sqlalchemy.orm import Session
from resources.authController import get_current_user
from models import models, get_db


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/oauth/authorize") 


@router.get('/instagram/me')
def facebook_user(request: Request):    
    data =  requests.get('https://graph.facebook.com/v11.0/me?fields=id,name&access_token={}'.format(BaseConfig.FB_token)).json()
    if data:
        name = data['name']
        id = data['id']
        return {'account_name': name, 'account_id':id}
    else:
        raise HTTPException(status_code=400, detail="Something went wrong")


@router.post('/instagram/users')
def instagram_pages(request:Request, Page_id : schemas.IGPage):
    data =  requests.get('https://graph.facebook.com/v11.0/{}/accounts?limit=100&access_token={}'.format(Page_id.facebook_page_id,BaseConfig.FB_token)).json()
    response = []
    for x in data['data']:
        page = {
            'name': x['name'],
            'id': x['id']
        }
        response.append(page)
    raise HTTPException(status_code=200, detail=response)

@router.post('/instagram/post_details')
def post_details(request: Request, IG_page : schemas.IGPage):
    data = IG_page_access_token(IG_page.facebook_page_id)
    raise HTTPException(status_code=200, detail=data)

@router.post('/instagram/analyzis')
def business_account_details(IG_username : schemas.IGSearch):
    value = IG_search_account(IG_username.username)
    base = value['business_discovery']
    post = base['media']['data']
    post_value = []
    hashtag_list = []

    for x in post:
        if 'caption' in x:
            content = x['caption']
            hashtags = extract_hashtags(content)

        else:
            content = 'No Caption for this post'
            hashtags = extract_hashtags(content)
        
        if 'media_url' in x:
            media_url = x['media_url']
        else:
            media_url = 'No media URL'

        post_details = {
            'creative_url'  : media_url,
            'creative_type' : x['media_type'],
            'ig_post_link'  : x['permalink'],
            'content'       : content,
            'hashtags_used' : hashtags,
            'post_likes'    : x['like_count'],
            'comment_count' : x['comments_count']
        }
        hashtag_list.append(hashtags)
        post_value.append(post_details)
    all_hashtags = hashtag_validation(hashtag_list)
    data = {
        'instagram_id'  : base['username'],
        'ig_followrs'   : base['followers_count'],
        'total_post'    : base['media_count'],
        'post_details'  : post_value,
        'all_hashtags'  : all_hashtags
    }
    raise HTTPException(status_code=200, detail=data)


@router.post('/instagram/createpost')
def instacreate_post(page_id: schemas.FBlikes ,media_url: schemas.FBmedia):
    data1 = IG_page_access_token_and_Id(page_id.facebook_page_id)
    id = data1['ig_business_id']
    url1 = "https://graph.facebook.com/v12.0/{}/media?image_url={}".format(id, media_url.facebook_media_url)

    payload={}
    headers = {
    'Authorization': 'Bearer {}'.format(BaseConfig.IG_token),
    'Cookie': 'fr=1LmLOnjYt3rgeKdsh..BhPwvK.de.AAA.0.0.BhPwvK.AWUix2Z3vqw; sb=ygs_YV2GbnbI2wjJZ2NROlTu'
    }

    response = requests.post(url1, headers=headers, data=payload).json()
    creation_id = response['id']
    url2 = "https://graph.facebook.com/v12.0/{}/media_publish?creation_id={}&access_token={}".format(id, creation_id, BaseConfig.IG_token)
    data = requests.post(url2).json()

    return data


@router.post('/instagram/hashtag')
def instahashtag_search(ht: schemas.IGHashtag):
    first_search = requests.get("https://graph.facebook.com/v12.0/ig_hashtag_search?user_id=17841444429586324&q={}&access_token={}".format(ht.hashtag, BaseConfig.IG_token)).json()
    d = first_search['data']
    dict=list(d)
    exctraction = dict[0]
    id = exctraction['id']
    data = requests.get("https://graph.facebook.com/v12.0/{}/recent_media?user_id=17841445708880282&fields=permalink,id,caption,media_url,media_type,timestamp,media_product_type,comments_count&access_token={}".format(id,BaseConfig.IG_token)).json()
    return data



@router.post('/instagram/public-me')
def facebook_user(request: Request, access : schemas.FBPublic):    
    data =  requests.get('https://graph.facebook.com/v11.0/me?fields=id,name&access_token={}'.format(access.accesstoken)).json()
    if data:
        name = data['name']
        id = data['id']
        return {'account_name': name, 'account_id':id}
    else:
        raise HTTPException(status_code=400, detail="Something went wrong")


@router.post('/instagram/public-users')
def instagram_pages(request:Request, Page_id : schemas.IGPage, access : schemas.FBPublic):
    data =  requests.get('https://graph.facebook.com/v11.0/{}/accounts?limit=100&access_token={}'.format(Page_id.facebook_page_id,access.accesstoken)).json()
    response = []
    for x in data['data']:
        page = {
            'name': x['name'],
            'id': x['id']
        }
        response.append(page)
    raise HTTPException(status_code=200, detail=response)


@router.post('/instagram/public-createpost')
def instacreate_post(projectuuid:str, page_id: str ,access : str, file: UploadFile = File(...),db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    data1 = IG_public_page_access_token_and_Id(page_id, access)
    id = data1['ig_business_id']
    platform_name ="instagram"
    image_url = media(current_user.uuid,projectuuid,platform_name,file)

    url1 = "https://graph.facebook.com/v12.0/{}/media?image_url={}".format(id, image_url)

    payload={}
    headers = {
    'Authorization': 'Bearer {}'.format(access),
    'Cookie': 'fr=1LmLOnjYt3rgeKdsh..BhPwvK.de.AAA.0.0.BhPwvK.AWUix2Z3vqw; sb=ygs_YV2GbnbI2wjJZ2NROlTu'
    }

    response = requests.post(url1, headers=headers, data=payload).json()
    creation_id = response['id']
    url2 = "https://graph.facebook.com/v12.0/{}/media_publish?creation_id={}&access_token={}".format(id, creation_id, access)
    
    data = requests.post(url2)
    if data.status_code == 200:
        status_report = 'Success'
    else:
        status_report = 'Failed'
    post_detail = models.Post(created_by=current_user.uuid, project_uuid=projectuuid, platform=platform_name ,upload_url=image_url,status=status_report)
    attachment_details = models.attachments(created_by=current_user.uuid, project_uuid=projectuuid,url=image_url)
    db.add(post_detail)
    db.add(attachment_details)
    db.commit()
    db.refresh(post_detail)
    db.refresh(attachment_details)
    return HTTPException(status_code=200, detail='Post Created Successfully')



@router.post('/instagram/profile_reach')
def test(page_id: schemas.FBlikes ,access : schemas.FBPublic, start_date: datetime = datetime.today(), end_date: datetime = datetime.today()):
    data1 = IG_public_page_access_token_and_Id(page_id.facebook_page_id, access.accesstoken)
    id = data1['ig_business_id']

    url = "https://graph.facebook.com/v12.0/{}/insights?metric= profile_views, reach&period=day&since={}&until={}&limit=1000".format(id,start_date,end_date)

    payload={}
    headers = {
    'Authorization': 'Bearer {}'.format(access.accesstoken),
    'Cookie': 'fr=1LmLOnjYt3rgeKdsh..BhPwvK.de.AAA.0.0.BhPwvK.AWUix2Z3vqw; sb=ygs_YV2GbnbI2wjJZ2NROlTu'
    }

    response = requests.get(url, headers=headers, data=payload).json()

    return response

@router.post('/instagram/followers_counts')
def insta_followers(page_id: schemas.FBlikes ,access : schemas.FBPublic, start_date: datetime = datetime.today(), end_date: datetime = datetime.today()):
    data1 = IG_public_page_access_token_and_Id(page_id.facebook_page_id, access.accesstoken)
    id = data1['ig_business_id']
    data = requests.get("https://graph.facebook.com/v12.0/{}/insights?metric=follower_count&period=day&since={}&until={}&limit=1000&access_token={}".format(id,start_date,end_date,access.accesstoken)).json()
    return data


@router.post('/instagram/daywise')
def insta_daywise(page_id: schemas.FBlikes ,access : schemas.FBPublic, start_date: datetime = datetime.today(), end_date: datetime = datetime.today()):
    data1 = IG_public_page_access_token_and_Id(page_id.facebook_page_id, access.accesstoken)
    id = data1['ig_business_id']
    data2 = requests.get("https://graph.facebook.com/v12.0/{}/media?fields=id,caption,permalink&since={}&until={}&access_token={}".format(id,start_date,end_date,access.accesstoken)).json()
    insights = []
    for x in data2['data']:
        id = x['id']
        data = requests.get("https://graph.facebook.com/v12.0/{}/insights?metric=reach,impressions,engagement&access_token={}".format(id,access.accesstoken)).json()
        final = {
            'post_id'  : id,
            'insights' : data
        }
        insights.append(final)
    return insights

@router.get('/test/')
def test(start_date: datetime = datetime.today()):
    timestamp = datetime.timestamp(start_date)
    return int(timestamp)