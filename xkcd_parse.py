# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 15:57:52 2014

@author: nikhilkardale
"""

import requests
from bs4 import BeautifulSoup
import os
from pprint import pprint
from random import randint
from time import sleep

def get_page(url, max_retries):
    for i in xrange(max_retries):
        r = requests.get(url)
        if r.status_code == 200:
            return r.content
    print r.status_code
    return False

def extract_link(url):
    html_content = get_page(url, 5)
    if html_content:
        parsed_data = BeautifulSoup(html_content)
        comic = parsed_data.find(id="comic").img
        comic_image = comic.get('src')
        comic_mouseover = comic.get('title')
        pos = parsed_data.title.text.find(':')
        comic_title = parsed_data.title.text[pos+2:]
        return comic_image, comic_mouseover, comic_title
    else:
        return False

def get_all_posts(url):
    posts = []
    html_content = get_page(url, 5)
    if html_content:
        parsed_data = BeautifulSoup(html_content).find(id='middleContainer')
        for x in parsed_data.find_all('a'):
            item = {'url': 'http://xkcd.com' + x['href'],
                    'publication_date': x['title'].encode('ascii', 'ignore'),
                    'name': x.text.encode('ascii', 'ignore')}
            posts.append(item)
        return posts
    else:
        return False

def download_image(src, localname):
    comic_image = get_page(src, 5)
    if not comic_image:
        return False
    f = open('out/' + localname, 'wb')
    f.write(comic_image)
    f.close()
    return True

def main():
    if not os.path.exists('out'):
        os.makedirs('out')
    
    all_posts = get_all_posts('http://xkcd.com/archive/')
    for post in all_posts[:5]:
        try:
            sleep(randint(1,6))
            img_src, img_mouseover_text, img_title = extract_link(post['url'])
            print '\nImage source: %s' % img_src
            print 'Image mouseover: %s' % img_mouseover_text
            print 'Image title: %s' % img_title
            filename = img_title.lower() + '.' + img_src[-3:].lower()
            if not os.path.exists(os.path.join(os.getcwd(), 'out/' + filename)):
                download_image(img_src, filename)
            print '\nDone for url: %s, %s' % (post['url'], post['name'])
            print '-----'
        except Exception as e:
            print '\nException in main: %s' % e
            print 'In URL: %s, %s' % (post['url'], post['name'])
    
    print '\n----- Done -----'

if __name__ == "__main__":
    main()