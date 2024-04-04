import json
import requests


def get_ID_user(access):
    url2 = "https://api.linkedin.com/v2/me?fields=id"
    headers = {
        'Authorization': 'Bearer {}'.format(str(access)),
        'Content-Type' : 'application/json',
        'Cookie': 'lidc="b=OB50:s=O:r=O:a=O:p=O:g=2583:u=235:x=1:i=1632212704:t=1632239978:v=2:sig=AQH2QjgSb6xkx7Dt13KaVKBM7CIMtdqM"; lidc="b=OB50:s=O:r=O:a=O:p=O:g=2583:u=235:x=1:i=1632213571:t=1632239978:v=2:sig=AQFH00F9n8WWVDKBsAHUhmbJq9C4bV_M"; bcookie="v=2&cf1cc966-342b-4dcc-8262-bd98fbfb3620"; lang=v=2&lang=en-us; lidc="b=OB50:s=O:r=O:a=O:p=O:g=2583:u=235:x=1:i=1632213552:t=1632239978:v=2:sig=AQF50lkQe_WWbrmlGS4YVA0c71pGcF8v"'
    }
    data1 = requests.get(url2, headers=headers).json() 
    return data1

def register_image(access, id):
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

def registered_image(access, uploadURL, url):
    headers = {
    'X-Restli-Protocol-Version': '2.0.0',
    'Content-Type': 'image/jpeg,image/png,image/gif',
    'Authorization': 'Bearer {}'.format(access),
    'Cookie': 'lidc="b=VB01:s=V:r=V:a=V:p=V:g=4478:u=1:x=1:i=1632388963:t=1632474913:v=2:sig=AQFfzgbi5zAJAtD3G2fAxZFbbMmbT106"; bcookie="v=2&cf1cc966-342b-4dcc-8262-bd98fbfb3620"; lang=v=2&lang=en-us; lidc="b=VB01:s=V:r=V:a=V:p=V:g=4478:u=1:x=1:i=1632388867:t=1632474913:v=2:sig=AQFVm4KH5dFChJNjHVB1SZymEMY-dqHc"'
    }
    with open(url, 'rb') as f:
        data = f.read()
    res = requests.post(uploadURL, data=data, headers=headers)

def upload_post(access,asset_id):
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
