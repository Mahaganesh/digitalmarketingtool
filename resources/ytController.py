import os
import requests
import requests.auth
from fastapi import APIRouter, HTTPException

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

router = APIRouter()


@router.get('/youtube/accesstoken')
async def youtube_accesstoken():
    try:
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=[
            "https://www.googleapis.com/auth/youtube.readonly",
            "https://www.googleapis.com/auth/youtube",
            "https://www.googleapis.com/auth/youtube.channel-memberships.creator",
            "https://www.googleapis.com/auth/youtube.force-ssl",
            "https://www.googleapis.com/auth/youtube.upload",
            "https://www.googleapis.com/auth/youtubepartner",
            "https://www.googleapis.com/auth/youtubepartner-channel-audit",
            "https://www.googleapis.com/auth/yt-analytics-monetary.readonly",
            "https://www.googleapis.com/auth/yt-analytics.readonly"
            ])

        flow.run_local_server(port=8080, prompt="consent")
        
        credentials = flow.credentials
        return HTTPException(status_code=200 , detail=credentials.__dict__)
    except:
        return HTTPException(status_code=400 ,detail='Access Denied')


'''https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=43894567942-beqldfq26jesjr2gl32joebtq5b7051m.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.channel-memberships.creator+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.force-ssl+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.upload+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutubepartner+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutubepartner-channel-audit&state=j25nq0r7QosWLkBsehUr24gPFccDSC&prompt=consent&access_type=online'''

'''https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=43894567942-beqldfq26jesjr2gl32joebtq5b7051m.apps.googleusercontent.com&redirect_uri=https://alphaadventise.com/&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.channel-memberships.creator+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.force-ssl+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.upload+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutubepartner+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutubepartner-channel-audit&state=j25nq0r7QosWLkBsehUr24gPFccDSC&prompt=consent&access_type=online'''

'''https://accounts.google.com/o/oauth2/auth?code=4/0AX4XfWj94aKRczzrmUNKPgDAKdYYJYqDVvemBLaDfRNIKsRJur1EE1HgtcrbOhFDcDQnEQ'''


@router.get('/youtube/url')
def youtube_url():
    return { 'yt-auth-url': 'https://accounts.google.com/o/oauth2/auth?response_type=token&client_id=43894567942-beqldfq26jesjr2gl32joebtq5b7051m.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.channel-memberships.creator+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.force-ssl+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.upload+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutubepartner+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutubepartner-channel-audit+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyt-analytics-monetary.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyt-analytics.readonly&state=UxCYTESxyaA8HVQan6WSELTW0S0uyy&prompt=consent&include_granted_scopes=true'}


@router.post('/youtube/me')
def youtube_me(accesstoken : str):
    url = "https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&mine=true"
    payload={}
    headers = {
    'Authorization': 'Bearer {}'.format(accesstoken)
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()

@router.post('/youtube/me/playlist')
def youtube_platlist(accesstoken : str):
    url = "https://www.googleapis.com/youtube/v3/playlists?part=id,snippet&mine=true"
    payload={}
    headers = {
    'Authorization': 'Bearer {}'.format(accesstoken)
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

@router.post('/youtube/all-video')
def youtube_all_video(accesstoken : str, channel_id : str):
    import requests

    url = "https://www.googleapis.com/youtube/v3/search?channelId={}&part=snippet&order=date".format(channel_id)

    payload={}
    headers = {
    'Authorization': 'Bearer {}'.format(accesstoken)
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()

@router.post("/google/test")
def google_test(id_token : str):
    import requests

    # id_token = input('ID Token : ')
    url = "https://oauth2.googleapis.com/tokeninfo?id_token={}".format(id_token)

    data = requests.get(url).json()

    return data