from re import I, S
import re
import time
import logging
import random
import string
import shutil

from resources.utils import  LI_access, LI_access2, LI_get_ID_user, LI_register_image, LI_registered_image, LI_upload_post,LI_organisation_upload_post, LI_organsation_register_image
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
import requests
from sqlalchemy.orm import immediateload
from sqlalchemy.sql.sqltypes import JSON
from starlette import responses
from starlette.types import Message
from config.base_config import BaseConfig
from models.schemas import schemas
import json

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/oauth/authorize")



@router.get('/LinkedIn/login/url')
def linikedin_login_url(request: Request):
    url1 = 'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=785g07boldeflt&redirect_uri=https://alphaadventise.com/&state=SomeRandomString&scope=r_liteprofile,w_member_social,r_emailaddress'
    url2 = 'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=78m9m1ob22a5r5&redirect_uri=https://alphaadventise.com/&state=SomeRandomString&scope=r_liteprofile,w_member_social,r_emailaddress,r_organization_social,rw_organization_admin,w_organization_social'
    data = {
        'url1' : url1,
        'url2' : url2
    }
    raise HTTPException(status_code=200, detail=data)


@router.post('/LinkedIn/access_token')
def linkedin_access_token(request: Request, auth: str):
    url = 'https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&code={}&redirect_uri=https://alphaadventise.com/&client_id=78m9m1ob22a5r5&client_secret=wVqkFP2kySrJGSKr'.format(auth)
    print(url)
    acces = requests.post(url).json()
    access = acces['access_token']
    data = {
        'access_token' : access
    }
    return data


# @router.post('/LinkedIn/access_token2')
# def linkedin_access_token(request: Request,auth: str):
#     data = LI_access2(auth)
#     return data


@router.post('/LinkedIn/me')
def linkedin_user_details(access : schemas.INaccess_token):
    url2 = "https://api.linkedin.com/v2/me"
    headers = {
        'Authorization': 'Bearer {}'.format(access.accesstoken),
        'Cookie': 'lidc="b=OB50:s=O:r=O:a=O:p=O:g=2583:u=235:x=1:i=1632212704:t=1632239978:v=2:sig=AQH2QjgSb6xkx7Dt13KaVKBM7CIMtdqM"; lidc="b=OB50:s=O:r=O:a=O:p=O:g=2583:u=235:x=1:i=1632213571:t=1632239978:v=2:sig=AQFH00F9n8WWVDKBsAHUhmbJq9C4bV_M"; bcookie="v=2&cf1cc966-342b-4dcc-8262-bd98fbfb3620"; lang=v=2&lang=en-us; lidc="b=OB50:s=O:r=O:a=O:p=O:g=2583:u=235:x=1:i=1632213552:t=1632239978:v=2:sig=AQF50lkQe_WWbrmlGS4YVA0c71pGcF8v"'
    }
    data = requests.get(url2, headers=headers).json() 
    return data


@router.post('/LinkedIn/createpost')
def linkedin_createpost(access_token : str, file: UploadFile = File(...)):
    data1 = LI_get_ID_user(access_token)
    id = data1['id']
    registered_response = LI_register_image(access_token, id)
    uploadURL = registered_response['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
    asset_id = registered_response['value']['asset']
    with open("/Users/mahaganesh/PycharmProjects/Alpha_adventise/media/"+file.filename, "wb") as image:
        shutil.copyfileobj(file.file, image)
    url = str("/Users/mahaganesh/PycharmProjects/Alpha_adventise/media/"+file.filename)
    LI_registered_image(access_token, uploadURL, url)
    response = LI_upload_post(access_token, asset_id)
    data = {
        'status' : 'Succesful',
        'response' : response
    }
    return data


@router.get('/LinkedIn/ogranisation-details')
def Linkedin_organisation_details(access_token : str):
    url = "https://api.linkedin.com/v2/organizationAcls?q=roleAssignee&projection=(elements*(*,roleAssignee~(localizedFirstName, localizedLastName), organization~(localizedName)))"

    payload={}
    headers = {
    'X-Restli-Protocol-Version': '2.0.0',
    'Authorization': 'Bearer {}'.format(access_token),
    'Cookie': 'lidc="b=TB31:s=T:r=T:a=T:p=T:g=3546:u=31:x=1:i=1635747404:t=1635831695:v=2:sig=AQGnEv7GeQb2G3C1gMCHYE92Sd-ZV3AQ"; bcookie="v=2&cf1cc966-342b-4dcc-8262-bd98fbfb3620"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()

@router.post('/LinkedIn/organisation-post')
def organisation_post(access_token : str, organisation : str, file: UploadFile = File(...)):
    data1 = LI_get_ID_user(access_token)
    id = data1['id']
    registered_response = LI_organsation_register_image(access_token, organisation)
    uploadURL = registered_response['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
    asset_id = registered_response['value']['asset']
    with open("/Users/mahaganesh/PycharmProjects/aa-apiservices/media/"+file.filename, "wb") as image:
        shutil.copyfileobj(file.file, image)
    url = str("/Users/mahaganesh/PycharmProjects/aa-apiservices/media/"+file.filename)
    LI_registered_image(access_token, uploadURL, url)
    response = LI_organisation_upload_post(access_token, asset_id, organisation)
    data = {
        'status' : 'Succesful',
        'response' : response
    }
    return data
