import requests
import requests.auth
from fastapi import APIRouter


router = APIRouter()



@router.get('/reddit-aa/url')
def reddit_url():
    url = 'https://www.reddit.com/api/v1/authorize?client_id=XVHTVG9eVHRLJ2ynucICxw&response_type=code&state=maha&redirect_uri=https://alphaadventise.com/&duration=permanent&scope=identity,edit,flair,history,modconfig,modflair,modlog,modposts,modwiki,mysubreddits,privatemessages,read,report,save,submit,subscribe,vote,wikiedit,wikiread'
    return url


@router.post('/reddit-aa/accesstoken')
def reddit_accesstoken(auth: str):
    client_auth = requests.auth.HTTPBasicAuth('XVHTVG9eVHRLJ2ynucICxw', 'QetswK-S9ByILeudoq90adF3u1d1pg')


    r = requests.post(
        url="https://www.reddit.com/api/v1/access_token",
        auth=client_auth,
        data={
            "grant_type": "authorization_code",
            "code": auth,
            "redirect_uri": "https://alphaadventise.com/"
        },
        headers={
            "User-Agent": "MG v1.0",
        }
    ).json()


    return r