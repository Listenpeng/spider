#Author: Listen
#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import re
import requests

tar_url = "https://rate.taobao.com/detailCommon.htm"
refer = "https://item.taobao.com/item.htm?" \
        "spm=a230r.1.14.119.76bf523Zih6Ob&id=548765652209&ns=1&abbucket=12"
NumID = re.findall(r"id=(\d+)\&",refer)
param = {
    "actionNumID": NumID,
    "userNumId": "43440508",
    "callback": "json_tbc_rate_summary"
}
header = {
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate, br",
    "Cache-Control":"no-cache",
    "Connection":"keep-alive",
    'Upgrade-Insecure-Requests': "1",
    'Referer': refer,
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:55.0) '
                 'Gecko/20100101 Firefox/55.0'
}

try:
    url_content = requests.get(url=tar_url,params=param,headers=header)
    print("url_content:",url_content.text)
except BaseException as e:
    pass