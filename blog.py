import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import re
import requests
import nltk
# nltk.download() # can comment out after first run
import textblob
import os
import altair as alt
import hidden

"""
Parameters:
    url - a url string representing valid API request

Returns:
    content - a list of strings representing HTML of blog
            posts
"""
def extract_content(url=hidden.url):
    resp = requests.get(url)
    resp = resp.json()
    content = list()
    next_page_token = True
    while next_page_token:
        for post in resp.get('items', None):
            content.append(post['content'].replace('\n', ''))
        next_page_token = resp.get('nextPageToken', None)
        if next_page_token:
            resp = requests.get(f'{url}&pageToken={next_page_token}').json()
    return content

"""
Parameters:
    url - a url string representing valid API request

Returns:
    content - a list of strings representing text of blog posts
"""
def extract_content_text_only(url=hidden.url):
    content = extract_content()
    for i in range(len(content)):
        content[i] = BeautifulSoup(content[i], 'html.parser').text
    return content