from codecs import backslashreplace_errors
import os
from re import I
import re
import sendgrid
import requests
import json

import shutil
from sendgrid.helpers.mail import Mail, Email, To, Content
from starlette import responses
from config.dev_config import Configuration
from config.base_config import BaseConfig
from models.schemas import schemas
from collections import Counter
from google.cloud import storage
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def email_sender1(sender_email, subject):
    try:
        sg = sendgrid.SendGridAPIClient(api_key=Configuration.SENDGRID_API_KEY)
        from_email = Email(BaseConfig.From_email)
        to_email = To(sender_email)
        subject = subject
        content = Content('text/plain', 'Email Test')
        mail = Mail(from_email, to_email, subject)
        mail.add_content(content)
        print('Sending email')
        response = sg.client.mail.send.post(request_body=mail.get())
        print(' email sent {}'.format(response._status_code))
        return { 'status': True }
    except Exception as e:
        # print(e.body)
        # print(str(e))
        return { 'status': False, 'error': {'message': 'Sending Mail Failed'}}

def email_sender(email):
    message = Mail(
    from_email='maha.ganesh@alphaadventise.com',
    to_emails = email,
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(api_key=Configuration.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        data = {
            'status code' : response.status_code,
            'body' : response.status_code,
            'headers' : response.headers
        }
        return data
    except Exception as e:
        print(e)
        return e

def page_access_token(page_id):
    pages_access_token = requests.get("https://graph.facebook.com/v12.0/{}?fields=access_token&access_token={}".format(page_id,BaseConfig.FB_token)).json()
    page_access_token = pages_access_token["access_token"]
    data = requests.get("https://graph.facebook.com/v12.0/{}/posts?fields=message,likes.summary(true),full_picture,comments,videos&access_token={}".format(page_id,page_access_token)).json() 
    return data

def public_page_access_token(page_id, access):
    pages_access_token = requests.get("https://graph.facebook.com/v12.0/{}?fields=access_token&access_token={}".format(page_id, access)).json()
    page_access_token = pages_access_token["access_token"]
    return page_access_token

def IG_page_access_token(page_id):
    pages_access_token = requests.get("https://graph.facebook.com/v12.0/{}?fields=access_token&access_token={}".format(page_id,BaseConfig.FB_token)).json()
    print(pages_access_token)
    page_access_token = pages_access_token["access_token"]
    ig_bussiness_account = requests.get("https://graph.facebook.com/v12.0/{}?fields=instagram_business_account&access_token={}".format(page_id,page_access_token)).json()
    business_account_id = ig_bussiness_account['instagram_business_account']['id']
    IG_media_id = requests.get("https://graph.facebook.com/v11.0/{}?fields=username,media&access_token={}".format(business_account_id,page_access_token)).json() 
    if IG_media_id:
        data = []
        for x in IG_media_id['media']['data']:
            media_id = x['id']
            detials = requests.get("https://graph.facebook.com/v12.0/{}?fields=media_type,media_url,username,caption,media_product_type,permalink,like_count,comments_count,comments&access_token={}".format(media_id,page_access_token)).json()
            data.append(detials)
    return data


def IG_search_account(username):
    data = requests.get("https://graph.facebook.com/v12.0/17841445708880282?fields=business_discovery.username({})%7Busername%2Cfollowers_count%2Cmedia_count%2Cmedia%7Bmedia_url%2Cmedia_type%2Cpermalink%2Clike_count%2Ccomments_count%2Ccaption%7D%7D&limit=10000&access_token={}".format(username,BaseConfig.IG_token)).json()
    return data
 
def extract_hashtags(text):
    regex = "#(\w+)"
    hashtag_list = re.findall(regex, text)
    hashtag1 = []
    for hashtag in hashtag_list:
        hashtag1.append(hashtag)
    return hashtag1

def hashtag_validation(hashtag_list):
    all_hashtags = []

    for hast in hashtag_list:
        for v in hast:
            all_hashtags.append(v)
    hashtag_counter = Counter()
    for word in all_hashtags:
        hashtag_counter[word] += 1
    hashtag_counter
    temp_list = []
    for i in all_hashtags:
        if i not in temp_list:
            temp_list.append(i)
    all_hashtags = temp_list
    hashtags = {
        'total_hashtags_used' : all_hashtags,
        'total_number'        : len(all_hashtags),
        'total_hashtags_count'      : hashtag_counter
    }   
    return hashtags   


def IG_page_access_token_and_Id(page_id):
    pages_access_token = requests.get("https://graph.facebook.com/v12.0/{}?fields=access_token&access_token={}".format(page_id,BaseConfig.FB_token)).json()
    print(pages_access_token)
    page_access_token = pages_access_token["access_token"]
    ig_bussiness_account = requests.get("https://graph.facebook.com/v12.0/{}?fields=instagram_business_account&access_token={}".format(page_id,page_access_token)).json()
    business_account_id = ig_bussiness_account['instagram_business_account']['id']
    data1 = {
        'ig_business_id' : business_account_id,
        'page_access_token' : page_access_token
    }
    return data1

def IG_public_page_access_token_and_Id(page_id, accesstoken):
    pages_access_token = requests.get("https://graph.facebook.com/v12.0/{}?fields=access_token&access_token={}".format(page_id, accesstoken)).json()
    print(pages_access_token)
    page_access_token = pages_access_token["access_token"]
    ig_bussiness_account = requests.get("https://graph.facebook.com/v12.0/{}?fields=instagram_business_account&access_token={}".format(page_id,page_access_token)).json()
    business_account_id = ig_bussiness_account['instagram_business_account']['id']
    data1 = {
        'ig_business_id' : business_account_id,
        'page_access_token' : page_access_token
    }
    return data1


def LI_access(auth):
    url = 'https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&code={}&redirect_uri=https://alphaadventise.com/&client_id=785g07boldeflt&client_secret=IvXFQoTz7P0zkuBr'.format(auth)
    print(url)
    acces = requests.post(url).json()
    access = acces['access_token']
    data = {
        'access_token' : access
    }
    return data

def LI_access2(auth):
    url = 'https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&code={}&redirect_uri=https://alphaadventise.com/&client_id=86ih8wgovyjuzn&client_secret=otpbvIC3tgIh9PoV'.format(auth)
    print(url)
    acces = requests.post(url).json()
    access = acces['access_token']
    data = {
        'access_token' : access
    }
    return data




#LinkedIn -------

def LI_get_ID_user(access):
    url2 = "https://api.linkedin.com/v2/me?fields=id"
    headers = {
        'Authorization': 'Bearer {}'.format(str(access)),
        'Content-Type' : 'application/json',
        'Cookie': 'lidc="b=OB50:s=O:r=O:a=O:p=O:g=2583:u=235:x=1:i=1632212704:t=1632239978:v=2:sig=AQH2QjgSb6xkx7Dt13KaVKBM7CIMtdqM"; lidc="b=OB50:s=O:r=O:a=O:p=O:g=2583:u=235:x=1:i=1632213571:t=1632239978:v=2:sig=AQFH00F9n8WWVDKBsAHUhmbJq9C4bV_M"; bcookie="v=2&cf1cc966-342b-4dcc-8262-bd98fbfb3620"; lang=v=2&lang=en-us; lidc="b=OB50:s=O:r=O:a=O:p=O:g=2583:u=235:x=1:i=1632213552:t=1632239978:v=2:sig=AQF50lkQe_WWbrmlGS4YVA0c71pGcF8v"'
    }
    data1 = requests.get(url2, headers=headers).json() 
    return data1

def LI_register_image(access, id):
    register_image = "https://api.linkedin.com/v2/assets?action=registerUpload"
    payload = json.dumps({
    "registerUploadRequest": {
        "recipes": [
        "urn:li:digitalmediaRecipe:feedshare-image"
        ],
        "owner": "urn:li:person:{}".format(id),
        "serviceRelationships": [
        {
            "relationshipType": "OWNER",
            "identifier": "urn:li:userGeneratedContent"
        }
        ]
    }
    })
    headers = {
    'X-Restli-Protocol-Version': '2.0.0',
    'Authorization': 'Bearer {}'.format(access),
    'Content-Type': 'application/json',
    'Cookie': 'lidc="b=VB01:s=V:r=V:a=V:p=V:g=4478:u=1:x=1:i=1632388945:t=1632474913:v=2:sig=AQEWRCUBjLSuGivn5GcDBfFVfCHtW5Yb"; bcookie="v=2&cf1cc966-342b-4dcc-8262-bd98fbfb3620"; lang=v=2&lang=en-us; lidc="b=VB01:s=V:r=V:a=V:p=V:g=4478:u=1:x=1:i=1632388867:t=1632474913:v=2:sig=AQFVm4KH5dFChJNjHVB1SZymEMY-dqHc"'
    }
    registered_response = requests.post(register_image, headers=headers, data=payload).json()
    return registered_response

def LI_registered_image(access, uploadURL, url):
    headers = {
    'X-Restli-Protocol-Version': '2.0.0',
    'Content-Type': 'image/jpeg,image/png,image/gif',
    'Authorization': 'Bearer {}'.format(access),
    'Cookie': 'lidc="b=VB01:s=V:r=V:a=V:p=V:g=4478:u=1:x=1:i=1632388963:t=1632474913:v=2:sig=AQFfzgbi5zAJAtD3G2fAxZFbbMmbT106"; bcookie="v=2&cf1cc966-342b-4dcc-8262-bd98fbfb3620"; lang=v=2&lang=en-us; lidc="b=VB01:s=V:r=V:a=V:p=V:g=4478:u=1:x=1:i=1632388867:t=1632474913:v=2:sig=AQFVm4KH5dFChJNjHVB1SZymEMY-dqHc"'
    }
    with open(url, 'rb') as f:
        data = f.read()
    res = requests.post(uploadURL, data=data, headers=headers)

def LI_upload_post(access,asset_id):
    url2 = "https://api.linkedin.com/v2/me?fields=id"
    headers = {
        'Authorization': 'Bearer {}'.format(str(access)),
        'Content-Type' : 'application/json',
        'Cookie': 'lidc="b=OB50:s=O:r=O:a=O:p=O:g=2583:u=235:x=1:i=1632212704:t=1632239978:v=2:sig=AQH2QjgSb6xkx7Dt13KaVKBM7CIMtdqM"; lidc="b=OB50:s=O:r=O:a=O:p=O:g=2583:u=235:x=1:i=1632213571:t=1632239978:v=2:sig=AQFH00F9n8WWVDKBsAHUhmbJq9C4bV_M"; bcookie="v=2&cf1cc966-342b-4dcc-8262-bd98fbfb3620"; lang=v=2&lang=en-us; lidc="b=OB50:s=O:r=O:a=O:p=O:g=2583:u=235:x=1:i=1632213552:t=1632239978:v=2:sig=AQF50lkQe_WWbrmlGS4YVA0c71pGcF8v"'
    }
    data1 = requests.get(url2, headers=headers).json() 
    id = data1['id']
    url = "https://api.linkedin.com/v2/ugcPosts"
    value = """
    Charan Raaj. #talentconnect
    Charan Raaj. #talentconnect

    Charan Raaj. #talentconnect
    """
    payload = {
        "author": "urn:li:person:{}".format(id),
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": value
                },
                "shareMediaCategory": "IMAGE",
                "media": [
                    {
                        "status": "READY",
                        "description": {
                            "text": "Center stage!"
                        },
                        "media": asset_id,
                        "title": {
                            "text": "LinkedIn Talent Connect 2021"
                        }
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    headers = {
    'X-Restli-Protocol-Version': '2.0.0',
    'content-type': 'application/json',
    'Content-Type': 'multipart/form-data',
    'Authorization': 'Bearer {}'.format(access),
    'Cookie': 'lidc="b=VB01:s=V:r=V:a=V:p=V:g=4478:u=1:x=1:i=1632394785:t=1632474913:v=2:sig=AQGdLP9brVvbXwmgaNvkcYB618PYzJty"; bcookie="v=2&cf1cc966-342b-4dcc-8262-bd98fbfb3620"; lang=v=2&lang=en-us; lidc="b=OB50:s=O:r=O:a=O:p=O:g=2583:u=240:x=1:i=1632389126:t=1632421125:v=2:sig=AQHwH2NGZrVyDZtoSp2_S1QglWa_UryJ"'
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload)).json()
    return response


def LI_organsation_register_image(access, id):
    register_image = "https://api.linkedin.com/v2/assets?action=registerUpload"
    payload = json.dumps({
    "registerUploadRequest": {
        "recipes": [
        "urn:li:digitalmediaRecipe:feedshare-image"
        ],
        "owner": id,
        "serviceRelationships": [
        {
            "relationshipType": "OWNER",
            "identifier": "urn:li:userGeneratedContent"
        }
        ]
    }
    })
    headers = {
    'X-Restli-Protocol-Version': '2.0.0',
    'Authorization': 'Bearer {}'.format(access),
    'Content-Type': 'application/json',
    'Cookie': 'lidc="b=VB01:s=V:r=V:a=V:p=V:g=4478:u=1:x=1:i=1632388945:t=1632474913:v=2:sig=AQEWRCUBjLSuGivn5GcDBfFVfCHtW5Yb"; bcookie="v=2&cf1cc966-342b-4dcc-8262-bd98fbfb3620"; lang=v=2&lang=en-us; lidc="b=VB01:s=V:r=V:a=V:p=V:g=4478:u=1:x=1:i=1632388867:t=1632474913:v=2:sig=AQFVm4KH5dFChJNjHVB1SZymEMY-dqHc"'
    }
    registered_response = requests.post(register_image, headers=headers, data=payload).json()
    return registered_response

def LI_organisation_upload_post(access,asset_id,organisation_id):
    # url2 = "https://api.linkedin.com/v2/me?fields=id"
    # headers = {
    #     'Authorization': 'Bearer {}'.format(str(access)),
    #     'Content-Type' : 'application/json',
    #     'Cookie': 'lidc="b=OB50:s=O:r=O:a=O:p=O:g=2583:u=235:x=1:i=1632212704:t=1632239978:v=2:sig=AQH2QjgSb6xkx7Dt13KaVKBM7CIMtdqM"; lidc="b=OB50:s=O:r=O:a=O:p=O:g=2583:u=235:x=1:i=1632213571:t=1632239978:v=2:sig=AQFH00F9n8WWVDKBsAHUhmbJq9C4bV_M"; bcookie="v=2&cf1cc966-342b-4dcc-8262-bd98fbfb3620"; lang=v=2&lang=en-us; lidc="b=OB50:s=O:r=O:a=O:p=O:g=2583:u=235:x=1:i=1632213552:t=1632239978:v=2:sig=AQF50lkQe_WWbrmlGS4YVA0c71pGcF8v"'
    # }
    # data1 = requests.get(url2, headers=headers).json() 
    # id = data1['id']
    url = "https://api.linkedin.com/v2/ugcPosts"
    value = """
    Charan Raaj. #talentconnect
    Charan Raaj. #talentconnect

    Charan Raaj. #talentconnect
    """
    payload = {
        "author": organisation_id,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": value
                },
                "shareMediaCategory": "IMAGE",
                "media": [
                    {
                        "status": "READY",
                        "description": {
                            "text": "Center stage!"
                        },
                        "media": asset_id,
                        "title": {
                            "text": "LinkedIn Talent Connect 2021"
                        }
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    headers = {
    'X-Restli-Protocol-Version': '2.0.0',
    'content-type': 'application/json',
    'Content-Type': 'multipart/form-data',
    'Authorization': 'Bearer {}'.format(access),
    'Cookie': 'lidc="b=VB01:s=V:r=V:a=V:p=V:g=4478:u=1:x=1:i=1632394785:t=1632474913:v=2:sig=AQGdLP9brVvbXwmgaNvkcYB618PYzJty"; bcookie="v=2&cf1cc966-342b-4dcc-8262-bd98fbfb3620"; lang=v=2&lang=en-us; lidc="b=OB50:s=O:r=O:a=O:p=O:g=2583:u=240:x=1:i=1632389126:t=1632421125:v=2:sig=AQHwH2NGZrVyDZtoSp2_S1QglWa_UryJ"'
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload)).json()
    return response


#LinkedIN -------




def SM_FB_profile_pic(access):
    url = "https://graph.facebook.com/v12.0/me?fields=id,name,picture,cover,can_post,page_token&access_token={}".format(access)
    payload={}
    headers = {
    'Cookie': 'fr=1LmLOnjYt3rgeKdsh..BhPwvK.de.AAA.0.0.BhPwvK.AWUix2Z3vqw; sb=ygs_YV2GbnbI2wjJZ2NROlTu'
    }
    data1 = requests.request("GET", url, headers=headers, data=payload).json()
    pic = data1['picture']['data']['url']
    cover = data1['cover']['source']
    name =  data1['name']

    data = {
        'profile' : pic,
        'cover' : cover,
        'name' : name
    }
    return data


def SM_IG_profile_pic(access, page_id):
    url = "https://graph.facebook.com/v12.0/{}?fields=instagram_business_account&access_token={}".format(page_id, access)
    data1 = requests.get(url).json()
    ig_id = data1['instagram_business_account']['id']
    url2 = "https://graph.facebook.com/v12.0/{}?fields=id,profile_picture_url,username,followers_count,follows_count&access_token={}".format(ig_id, access)
    data2 = requests.get(url2).json()
    profile_pic = data2['profile_picture_url']
    name = data2['username']
    followers = data2['followers_count']
    follows = data2['follows_count']
    data = {
        'ig_id' : ig_id,
        'name': name,
        'profile': profile_pic,
        'followers' : followers,
        'follows' : follows
    }
    return data



def media(user_id, projectname, platform, file):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./dev-alphaadventise-340706-a41d2385bd68.json"
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('dev-alphaadventise-340706')
    a = bucket.get_blob('{}+{}/{}/{}'.format(user_id,projectname,platform,file.filename))
    if a:
        d = '{}+{}/{}/{}'.format(user_id,projectname,platform,file.filename)
        blob=bucket.blob(d) 
        blob.upload_from_file(file.file)
        blob.make_public() 
        return blob.public_url
    else:
        d = '{}+{}/{}/{}'.format(user_id,projectname,platform,file.filename)
        blob=bucket.blob(d) 
        blob.upload_from_file(file.file)
        blob.make_public() 

        return blob.public_url