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

"""
Parameters:
    num_files - number of .md files to generate (more files = smaller
                files, which can be better for some md renderers); default 1
    space_between - number of blank lines between entries; default 4
    output_dir - directory for generated files to be placed; default
                ./markdown_files in CWD, which will be generated if 
                it doesn't already exist

Returns:
    None
"""
def generate_markdown_files(num_files=1, space_between=4, output_dir='./markdown_files/'):
    if num_files < 1:
        num_files = 1
    content = extract_content()
    num_posts = len(content)
    increment = num_posts // num_files
    joiner = "<br/>" * space_between
    file_sizes = list()
    i, j = 0, increment
    while j <= num_posts:
        file_sizes.append((i,j))
        i = j
        j += increment
    for i,j in file_sizes:
        if i / increment == num_files - 1:
            text = joiner.join(content[i:])
        else:
            text = joiner.join(content[i:j])
        text = text.strip()
        file = open(f'./markdown_files/blog_posts{i}.md', 'w')
        file.write(text)
        file.close()
    return

"""
Parameters:
    None

Returns:
    None

Modifies:
    After markdown files have been generated through generate_markdown_files(),
    remove_links() writes new files which have removed links but preserved
    the underlying text for titles, authors, and ratings.
"""
def remove_links():
    files = os.listdir('Desktop')
    files = [f for f in files if 'blog' in f]
    text_list = list()
    for file in files:
        matches, titles = list(), list()
        author_matches, authors = list(), list()
        rating_matches, ratings = list(), list()
        with open(f'./markdown_files/{file}', 'r') as f:
            lines = f.read()
            matches.extend(
                re.findall('<a href="http://www.goodreads.com/book/show/[0-9]*">[0-9A-Za-z.!-:,&\' ]*</a>', lines))
            matches.extend(
                re.findall('<a href="https://www.goodreads.com/book/show/[0-9]*">[0-9A-Za-z.!-:,&\' ]*</a>', lines))
            titles.extend(
                re.findall('<a href="http://www.goodreads.com/book/show/[0-9]*">([0-9A-Za-z.!-:,&\' ]*)</a>', lines))
            titles.extend(
                re.findall('<a href="https://www.goodreads.com/book/show/[0-9]*">([0-9A-Za-z.!-:,&\' ]*)</a>', lines))
            author_matches.extend(
                re.findall('<a href="http://www.goodreads.com/author/show/[0-9]*">[0-9A-Za-z.!-:,&\' ]*</a>', lines))
            author_matches.extend(
                re.findall('<a href="https://www.goodreads.com/author/show/[0-9]*">[0-9A-Za-z.!-:,&\' ]*</a>', lines))
            authors.extend(
                re.findall('<a href="http://www.goodreads.com/author/show/[0-9]*">([0-9A-Za-z.!-:,&\' ]*)</a>', lines))
            authors.extend(
                re.findall('<a href="https://www.goodreads.com/author/show/[0-9]*">([0-9A-Za-z.!-:,&\' ]*)</a>', lines))
            rating_matches.extend(
                re.findall('<a href="http://www.goodreads.com/review/show/[0-9]*">[0-9A-Za-z.!-:,&\' ]*</a>', lines))
            rating_matches.extend(
                re.findall('<a href="https://www.goodreads.com/review/show/[0-9]*">[0-9A-Za-z.!-:,&\' ]*</a>', lines))
            ratings.extend(
                re.findall('<a href="http://www.goodreads.com/review/show/[0-9]*">([0-9A-Za-z.!-:,&\' ]*)</a>', lines))
            ratings.extend(
                re.findall('<a href="https://www.goodreads.com/review/show/[0-9]*">([0-9A-Za-z.!-:,&\' ]*)</a>', lines))
        tm = list(zip(titles, matches))
        am = list(zip(authors, author_matches))
        rm = list(zip(ratings, rating_matches))
        for title, pattern in tm:
            lines = re.sub(pattern, title, lines)
        for author, pattern in am:
            lines = re.sub(pattern, author, lines)
        for rat, pattern in rm:
            lines = re.sub(pattern, rat, lines)
        text_list.append(lines)
    i = 1
    for text in text_list:
        file = open(f'Desktop/blog_posts{i}.md', 'w')
        file.write(text)
        file.close()
        i += 1
    return