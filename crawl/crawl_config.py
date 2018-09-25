# -*- coding: utf-8 -*-
"""
__author__ = z0305
__date__ = 08/26/2018
"""

COOKIE = "cy=1; cye=shanghai; _lxsdk_cuid=1653dcc99a6c8-04ff4f92706bc4-1c2f1702-2f4f0c-1653dcc99a6bb; _lxsdk=1653dcc99a6c8-04ff4f92706bc4-1c2f1702-2f4f0c-1653dcc99a6bb; _hc.v=c668bd43-a103-53a2-3ccb-2d01ad06f352.1534340144; _lxsdk_s=1653dcc99ae-1-d99-0e5%7C%7C48"

# html保存路径
PATH_HTML_DIR = "/output/html_cached"

# 星级商户评价
STAR_SCORE = {u"五星商户": 10, u"准五星商户": 9, u"四星商户": 8, u"准四星商户": 7,
              u"三星商户": 6, u"准三星商户": 5, u"二星商户": 4, u"准二星商户": 3, u"一星商户": 2, u"准一星商户": 1,
              }


# # 20180820定义的字符串对应编号, 怀疑网站会定期更改(怀疑是有几个固定版本, 穷举可以解决), 20180917: 已证实该处用不着
# STRING_NUM = {"fn-67HV": 0, "1": 1, "fn-cMXT": 2,  "fn-6OZv": 3, "fn-JG8T": 4,
#               "fn-UqkY": 5, "fn-QanZ": 6, "fn-Kwvz": 7, "fn-Lmh3": 8, "fn-JEFc": 9
#               }

""" 反爬虫header对比 """
# 正常结果:
# {'Content-Language': 'zh-CN', 'Content-Encoding': 'gzip', 'Transfer-Encoding': 'chunked', 'Set-Cookie':
#  's_ViewType=10; Domain=.dianping.com; Expires=Wed, 16-Sep-2020 02:57:47 GMT; Path=/',
# 'Vary': 'User-Agent, Accept-Encoding', 'Keep-Alive': 'timeout=5', 'Server': 'DPweb', 'Connection': 'keep-alive',
# 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Date': 'Mon, 17 Sep 2018 02:57:48 GMT',
# 'Content-Type': 'text/html;charset=UTF-8'}
# html长度: 271321
# 异常结果:
# {'Content-Encoding': 'gzip', 'Transfer-Encoding': 'chunked', 'Expires': 'Sun, 17 Sep 2017 02:56:25 GMT',
# 'Server': 'Tengine','Last-Modified': 'Wed, 15 Aug 2018 12:55:59 GMT', 'Connection': 'keep-alive',
# 'Cache-Control': 'no-cache, private, no-cache, no-store, proxy-revalidate',
# 'Date': 'Mon, 17 Sep 2018 02:56:25 GMT', 'Content-Type': 'text/html'}
# html长度: 6656
