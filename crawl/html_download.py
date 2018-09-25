# -*- coding: utf-8 -*-
"""
__author__ = z0305
__date__ = 08/23/2018 
"""

import time
import os, io
from random import uniform

import requests
from crawl_config import COOKIE, PATH_HTML_DIR
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def url_download(url_):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.dianping.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
        "Upgrade-Insecure-Requests": "1",
        "Cookie": COOKIE,
    }

    time.sleep(uniform(2, 3))
    r_ = requests.get(url_, headers=headers, verify=False, stream=True)
    if r_.headers.get("Set-Cookie"):
        content_ = r_.content.decode("utf-8")
        return content_
    else:
        return -1


def html_cached(url_req_):
    """ 将访问过的url缓存到本地, 若不存在则爬虫 """
    html_dir_ = os.path.join(PROJECT_PATH + PATH_HTML_DIR)
    if not os.path.exists(html_dir_):
        os.mkdir(html_dir_)

    url_labels_ = url_req_.split("/")
    if len(url_labels_) == 6:
        html_city_dir_ = os.path.join(html_dir_, url_labels_[-3])
        if not os.path.exists(html_city_dir_):
            os.mkdir(html_city_dir_)

        filename = "{}/{}_{}.html".format(url_labels_[-3], url_labels_[-2], url_labels_[-1])
        path_html_ = os.path.join(html_dir_, filename)
    elif len(url_labels_) == 5:
        html_city_dir_ = os.path.join(html_dir_, url_labels_[-2])
        if not os.path.exists(html_city_dir_):
            os.mkdir(html_city_dir_)

        filename = "{}/{}.html".format(url_labels_[-2], url_labels_[-1])
        path_html_ = os.path.join(html_dir_, filename)
    else:
        raise Exception()

    # 如果文件缓存过了，读文件并返回
    if os.path.exists(path_html_):
        with io.open(path_html_, 'r', encoding="utf-8") as f:
            s = f.read()
            return s
    else:
        html = url_download(url_req_)
        if html != -1:
            with io.open(path_html_, 'w', encoding="utf-8") as f:
                f.write(html)
            return html
        else:
            print(u'{}下载失败'.format(filename))
            return -1


if __name__ == '__main__':
    url = "http://www.dianping.com/beijing/ch10"
    data = html_cached(url)
    # data = url_download(url)
    print(len(data))
    print(type(data))
