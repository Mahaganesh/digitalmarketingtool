# import imp
# from turtle import ht
# from seoanalyzer import analyze

# from seoanalyzer import http

# def test_http():
#     assert http.http.get('https://www.poorvika.com/sitemap.xml')
# print(test_http())
 
# site = "https://poorvika.com"
# site_map = "https://poorvika.com/sitemap.xml"


 
# site_map = "xml-sitemaps.com/download/casereads.com-8eedebb37/sitemap.xml?view=1"
# print('Inprogress.....')
# from bs4 import BeautifulSoup
# from urllib.request import urlopen

# url = 'https://poorvika.com/'

# html = urlopen(url)
# data = BeautifulSoup(html, "html.parser")
# print(data)

# output = analyze(url)

# print(output)

# import sys
# import logging
# from pysitemap import crawler
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
# if __name__ == '__main__':
#     if '--iocp' in sys.argv:
#         from asyncio import events, windows_events
#         sys.argv.remove('--iocp')
#         logging.info('using iocp')
#         el = windows_events.ProactorEventLoop()
#         events.set_event_loop(el)
 

#         root_url = sys.argv[1]
# root_url = 'https://www.poorvika.com/'
# crawler(root_url, out_file='sitemap.xml', exclude_urls=[".pdf", ".jpg", ".zip"])


import requests
import json
from bs4 import BeautifulSoup

URLS = ['https://www.poorvika.com/']
ATTRIBUTES = ['description', 'keywords', 'Description', 'Keywords','src','href','url','Src','href','url']

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

print(json.dumps(collected_data, indent=3))
# for entry in collected_data:
#     print(entry)