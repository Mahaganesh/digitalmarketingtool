from os import access
from re import escape
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
import requests
import json
import shutil
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.sqltypes import NullType
from models.schemas import schemas
import datetime
from datetime import date
from models import models, get_db
from resources.authController import get_current_user
from resources.utils import media



router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/oauth/authorize")


@router.get('/pinterest/login/url')
def pin_login():
    url = "https://www.pinterest.com/oauth/?client_id=1473190&redirect_uri=https://alphaadventise.com/&response_type=code&scope=boards:read,pins:read,user_accounts:read,boards:write,pins:write&state=connected"
    return url

@router.post('/pinterest/access-token')
def pin_access_token(code: schemas.Pinauth):
    url = "https://api.pinterest.com/v5/oauth/token"
    payload='code={}&grant_type=authorization_code&redirect_uri=https://alphaadventise.com/'.format(code.auth_code)
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic MTQ3Mjg1MTozZmY1YWY1MDIzMjAzZjQyZGJmNDJlODA5YTYyMGZiZGJkYTA0N2Ez',
    'Cookie': '_auth=0; _pinterest_sess=TWc9PSZOdktyRFpCRTkrVTNnRXJYeW56aFNFQjFQNTVuN3MzZkVjdmwwT25UZDlVUWZhU215VWlnK0dWNjJHa1pLak1JRGg3N0lUR2ZiTlpuRE90YVIyQWFwWGx3N3RVVzQxazk0RzZTeU5sdG91RVlkNUR4cCtsSzlEZFVTdlFoRFpHQyZxbU5EZHgrTHAxMlJ4QnJQb2NRamswZGcyeUU9; _ir=0'
    }
    response = requests.post(url, headers=headers, data=payload).json()
    return response


@router.post('/pinterest/create-board')
def create_board(name: str, description: str, access: schemas.Pinaccess):
    url = "https://api.pinterest.com/v5/boards"

    payload = json.dumps({
    "name": name,
    "description": description,
    "privacy": "PUBLIC"
    })
    headers = {
    'Authorization': 'Bearer {}'.format(access.access_token),
    'Content-Type': 'application/json',
    'Cookie': '_auth=0; _pinterest_sess=TWc9PSZOdktyRFpCRTkrVTNnRXJYeW56aFNFQjFQNTVuN3MzZkVjdmwwT25UZDlVUWZhU215VWlnK0dWNjJHa1pLak1JRGg3N0lUR2ZiTlpuRE90YVIyQWFwWGx3N3RVVzQxazk0RzZTeU5sdG91RVlkNUR4cCtsSzlEZFVTdlFoRFpHQyZxbU5EZHgrTHAxMlJ4QnJQb2NRamswZGcyeUU9; _ir=0'
    }
    response = requests.post(url, headers=headers, data=payload)
    
    return response.json()



@router.post('/pinterest/get_boards')
def get_board(access: schemas.Pinaccess):
    url = "https://api.pinterest.com/v5/boards"
    payload={}
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer {}'.format(access.access_token),
    'Cookie': '_auth=0; _pinterest_sess=TWc9PSZOdktyRFpCRTkrVTNnRXJYeW56aFNFQjFQNTVuN3MzZkVjdmwwT25UZDlVUWZhU215VWlnK0dWNjJHa1pLak1JRGg3N0lUR2ZiTlpuRE90YVIyQWFwWGx3N3RVVzQxazk0RzZTeU5sdG91RVlkNUR4cCtsSzlEZFVTdlFoRFpHQyZxbU5EZHgrTHAxMlJ4QnJQb2NRamswZGcyeUU9; _ir=0'
    }
    response = requests.get(url, headers=headers, data=payload).json()
    return response


@router.post('/pinterest/board-pin-list')
def boards_pin_list(board: schemas.Pinboard, access: schemas.Pinaccess):

    url = "https://api.pinterest.com/v5/boards/{}/pins".format(board.board_id)

    payload={}
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer {}'.format(access.access_token),
    'Cookie': '_auth=0; _pinterest_sess=TWc9PSZOdktyRFpCRTkrVTNnRXJYeW56aFNFQjFQNTVuN3MzZkVjdmwwT25UZDlVUWZhU215VWlnK0dWNjJHa1pLak1JRGg3N0lUR2ZiTlpuRE90YVIyQWFwWGx3N3RVVzQxazk0RzZTeU5sdG91RVlkNUR4cCtsSzlEZFVTdlFoRFpHQyZxbU5EZHgrTHAxMlJ4QnJQb2NRamswZGcyeUU9; _ir=0'
    }

    response = requests.get(url, headers=headers, data=payload).json()

    return response

@router.delete('/pinterest/delete-board')
def delete_board(board: schemas.Pinboard, access: schemas.Pinaccess):
    url = "https://api.pinterest.com/v5/boards/{}".format(board.board_id)
    payload={}
    headers = {
    'Authorization': 'Bearer {}'.format(access.access_token),
    'Cookie': '_auth=0; _pinterest_sess=TWc9PSZOdktyRFpCRTkrVTNnRXJYeW56aFNFQjFQNTVuN3MzZkVjdmwwT25UZDlVUWZhU215VWlnK0dWNjJHa1pLak1JRGg3N0lUR2ZiTlpuRE90YVIyQWFwWGx3N3RVVzQxazk0RzZTeU5sdG91RVlkNUR4cCtsSzlEZFVTdlFoRFpHQyZxbU5EZHgrTHAxMlJ4QnJQb2NRamswZGcyeUU9; _ir=0'
    }
    response = requests.delete(url, headers=headers, data=payload)
    if response.status_code == 204:
        data= {
            'status': 'successfully'
        }
    else:
        data= {
            'status': response.json()
        }
    return data
  

@router.post('/pinterest/pin_create')
def pin_create(title: str,description: str, access: str, projectuuid: str,board_id: str,file: UploadFile = File(...), db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    platform_name = "pinterest"
    image_url = media(current_user.uuid,projectuuid,platform_name,file)
    url = "https://api.pinterest.com/v5/pins"
    payload = json.dumps({
    "link": None,
    "title": title,
    "description": description,
    "alt_text": "string",
    "board_id": board_id,
    "board_section_id": None,
    "media_source": {
        "source_type": "image_url",
        "url": "{}".format(image_url)
    }
    })
    headers = {
    'Authorization': 'Bearer {}'.format(access),
    'Content-Type': 'application/json',
    'Cookie': '_auth=0; _pinterest_sess=TWc9PSZOdktyRFpCRTkrVTNnRXJYeW56aFNFQjFQNTVuN3MzZkVjdmwwT25UZDlVUWZhU215VWlnK0dWNjJHa1pLak1JRGg3N0lUR2ZiTlpuRE90YVIyQWFwWGx3N3RVVzQxazk0RzZTeU5sdG91RVlkNUR4cCtsSzlEZFVTdlFoRFpHQyZxbU5EZHgrTHAxMlJ4QnJQb2NRamswZGcyeUU9; _ir=0'
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        status_report = 'Success'
    else:
        status_report = 'Failed'
    post_detail = models.Post(created_by=current_user.uuid, project_uuid=projectuuid, platform=platform_name ,upload_url=image_url,status=status_report)
    attachment_details = models.attachments(created_by=current_user.uuid, project_uuid=projectuuid, url=image_url)
    db.add(post_detail)
    db.add(attachment_details)
    db.commit()
    db.refresh(post_detail)
    db.refresh(attachment_details)
    return response.json() 
 
@router.post('/pinterest/analyze')
def pinterest_analyze(access: schemas.Pinaccess, start_date: date = datetime.date.today(), end_date: date = datetime.date.today()):
    url = "https://api.pinterest.com/v5/user_account/analytics?start_date={}&end_date={}".format(start_date, end_date)
    payload={}
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer {}'.format(access.access_token),
    'Cookie': '_auth=0; _pinterest_sess=TWc9PSZOdktyRFpCRTkrVTNnRXJYeW56aFNFQjFQNTVuN3MzZkVjdmwwT25UZDlVUWZhU215VWlnK0dWNjJHa1pLak1JRGg3N0lUR2ZiTlpuRE90YVIyQWFwWGx3N3RVVzQxazk0RzZTeU5sdG91RVlkNUR4cCtsSzlEZFVTdlFoRFpHQyZxbU5EZHgrTHAxMlJ4QnJQb2NRamswZGcyeUU9; _ir=0'
    }
    response = requests.get(url, headers=headers, data=payload).json()
    return response