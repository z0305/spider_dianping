# -*- coding: utf-8 -*-
"""
__author__ = z0305
__date__ = 08/26/2018
"""

import time

from lxml import etree
from html_download import html_cached
from crawl_config import STAR_SCORE


def get_restaurant_details(url_):
    """
    获取餐厅详细信息：餐厅名称，星级标准，评论量，人均价格，类别，所属商区，具体位置，推荐菜，评价指标
    :param url_:   str, e.g.: http://www.dianping.com/shanghai/ch10
    :return:       list, 内部dict
    """
    content_ = html_cached(url_)
    if content_ != -1:
        root = etree.HTML(content_)
        rest_nodes = root.xpath('.//div[@id="shop-all-list"]/ul/li')

        restaurant_details_result = []
        for line in rest_nodes:
            restaurant_details_dict_ = {}
            name_nodes = line.xpath('.//div[@class="tit"]/a')
            url = name_nodes[0].attrib["href"]  # 餐厅详情链接
            name = name_nodes[0].attrib["title"]  # 餐厅名称
            restaurant_details_dict_["url"] = url
            restaurant_details_dict_[u"餐厅名称"] = name

            rank_starts = line.xpath('.//span/@title')  # 餐厅等级, 如五星商户
            restaurant_details_dict_[u"星级标准"] = STAR_SCORE[rank_starts[0]]

            comment_price_node = line.xpath('.//div[@class="comment"]/a/b/text()')
            try:
                comment = comment_price_node[0]  # 评论数量
                price = comment_price_node[1].replace(u"￥", "")  # 平均价格
                restaurant_details_dict_[u"评论量"] = comment
                restaurant_details_dict_[u"人均价格"] = price
            except IndexError:  # 广告类或新商店， 暂无数据
                pass

            tag_addr = line.xpath('.//div[@class="tag-addr"]/a/span/text()')
            restaurant_details_dict_[u"类别"] = tag_addr[0]      # 所属菜系, 比如日本菜
            try:
                restaurant_details_dict_[u"所属商区"] = tag_addr[1]  # 热门商区
            except IndexError:
                pass

            addr = line.xpath('.//div[@class="tag-addr"]/span/text()')[0]  # 具体位置
            restaurant_details_dict_[u"具体位置"] = addr

            comment_list = line.xpath('.//span[@class="comment-list"]/span/b/text()')  # 评价指标
            if len(comment_list) > 0:
                restaurant_details_dict_[u"口味"] = comment_list[0]
                restaurant_details_dict_[u"环境"] = comment_list[1]
                restaurant_details_dict_[u"服务"] = comment_list[2]

            recommend = line.xpath('.//div[@class="recommend"]/a/text()')  # list, 推荐菜
            restaurant_details_dict_[u"推荐菜"] = ",".join(recommend)
            restaurant_details_result.append(restaurant_details_dict_)
        return restaurant_details_result
    else:
        return -1


def get_restaurant_classify(url_):
    """ 按类别或商区分别爬虫 """
    content_ = html_cached(url_)
    if content_ != -1:
        root = etree.HTML(content_)

        # 美食分类
        classfy_nodes = root.xpath('.//div[@id="classfy"]/a')
        classify_result_list_ = [{"url": ii.attrib["href"], u"分类": ",".join(ii.xpath(".//span/text()"))} for ii in classfy_nodes]

        # 热门商区
        bussi_nodes = root.xpath('.//div[@id="bussi-nav"]/a')
        bussi_result_list_ = [{"url": ii.attrib["href"], u"热门商区": ",".join(ii.xpath(".//span/text()"))} for ii in bussi_nodes]

        # 行政区
        region_nodes = root.xpath('.//div[@id="region-nav"]/a')
        region_result_list_ = [{"url": ii.attrib["href"], u"行政区": ",".join(ii.xpath(".//span/text()"))} for ii in region_nodes]

        # 地铁线
        metro_nodes = root.xpath('.//div[@id="metro-nav"]/a')
        metro_result_list_ = [{"url": ii.attrib["href"], u"地图线": ii.xpath(".//span/text()")} for ii in metro_nodes]
        return classify_result_list_, bussi_result_list_, region_result_list_, metro_result_list_
    else:
        return -1


if __name__ == '__main__':
    import uniout

    start = time.time()
    url = "http://www.dianping.com/beijing/ch10"
    # url = "http://www.dianping.com/shijiazhuang/ch10/g117"

    classify_result, bussi_result, region_result, metro_result = get_restaurant_classify(url)
    # data = get_restaurant_details(url)
    for ii in classify_result:
        print("===")
        print(ii)

    print("time: {:.2f}s".format(time.time() - start))


