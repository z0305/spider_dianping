# -*- coding: utf-8 -*-
"""
__author__ = zhengh
__date__ = 04/26/2018
__site__ = https://mp.weixin.qq.com/s/dkaV4VZ1QBzcsi9gXvCRdw (Python告诉你上海有哪些高性价比的西餐厅)
           https://github.com/pythonml/restaurant
"""

import io
import time
import uniout
import json

from utils.common_ import url_download


def main():
    url = "http://www.dianping.com/shanghai/ch10/g116"

    root = url_download(url)
    distr_nodes = root.xpath('.//div[@id="region-nav"]')
    distr_node = distr_nodes[0]

    # 每个区区名和URL链接
    result_distr_url_ = [{"name": node.attrib["data-click-title"], "url": node.attrib["href"]} for node in distr_node]

    result_sub = []
    for item in result_distr_url_[:2]:
        distr_name = item["name"]  # 每个区区名
        distr_url = item["url"]  # 每个区对应URL链接
        root = url_download(distr_url)
        sub_nodes = root.xpath('.//div[@id="region-nav-sub"]/a[@data-cat-id]')
        for node in sub_nodes:
            url = node.attrib["href"]
            name = node.xpath('./span')[0].text
            # 每个区中每个热门商区的URL
            result_sub.append({"district": distr_name, "sub": name, "url": url})

    url_file = io.open(u"output/大众点评.json", "w", encoding="UTF-8")
    for line in result_sub:
        url = line["url"]
        root = url_download(url)
        rest_nodes = root.xpath('.//div[@id="shop-all-list"]/ul/li')
        if len(rest_nodes) == 0:
            break
        for node in rest_nodes:
            a_nodes = node.xpath('.//div[@class="tit"]/a')
            if len(a_nodes) == 0:
                continue
            url = a_nodes[0].attrib["href"]
            name = a_nodes[0].attrib["title"]
            url_dict = {"url": url, "title": name.encode("UTF-8"), u"热门商区": line["sub"], u"district": line["district"]}
            url_str = json.dumps(url_dict, encoding='UTF-8', ensure_ascii=False)
            url_file.write(url_str + u"\n")


if __name__ == '__main__':
    start = time.time()
    main()

    print("time: {:.2f}s".format(time.time() - start))
