# Author: Listen
# !/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool
import pandas as pd

def get_one_page(url):
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) Applewebkit/537.36' \
                     '(KHTML like Gecko) Chrome/45.0.2454.101 Safari/537.36'
        headers = {'User-Agent': user_agent}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?">(\d+)</i>.*?src="(.*?)".*?<a.*?>'
                         +'(.*?)</a>.*?<p.*?star">(.*?)</p>.*?releasetime">(.*?)'
                         +'</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>',re.S)
    iterms = re.findall(pattern, html)
    for iterm in iterms:
        yield {
            'index': iterm[0],
            'image': iterm[1],
            'title': iterm[2],
            'actor': iterm[3].strip()[3:],
            'time': iterm[4].strip()[5:],
            'score': iterm[5] + iterm[6],}


def write_to_file(content):
    with open('result.csv', 'a', encoding='utf-8') as f :
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

def main(offset):
    url = 'http://maoyan.com/board/4?offset={0}'.format(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)



if __name__ == '__main__':
    offest = [ i*10 for i in range(10)]
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])




