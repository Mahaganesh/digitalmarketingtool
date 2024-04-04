from typing import List
import requests
import json
from bs4 import BeautifulSoup

from fastapi import APIRouter


router = APIRouter()



@router.post('/website-keywords/')
def website_keywords_extraction(website_url: str):
    URLS = [website_url]
    ATTRIBUTES = ['description', 'keywords', 'Description', 'Keywords']

    collected_data = []

    for url in URLS:
        entry = {'url': url}
        try:
            r = requests.get(url)
        except Exception as e:
            print('Could not load page {}. Reason: {}'.format(url, str(e)))
            continue
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            meta_list = soup.find_all("meta")
            for meta in meta_list:
                if 'name' in meta.attrs:
                    name = meta.attrs['name']
                    if name in ATTRIBUTES:
                        entry[name.lower()] = meta.attrs['content']
            if len(entry) == 3:
                collected_data.append(entry)
            else:
                print('Could not find all required attributes for URL {}'.format(url))
        else:
            print('Could not load page {}.Reason: {}'.format(url, r.status_code))
    print('Collected meta attributes (TODO - push to DB):')

    # data = json.dumps(collected_data, indent=3)
    return collected_data
# for entry in collected_data:
#     print(entry)