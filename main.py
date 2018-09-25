# -*- coding: utf-8 -*-
"""
__author__ = zhengh
__date__ = 08/26/2018
__site__ = https://mp.weixin.qq.com/s/dkaV4VZ1QBzcsi9gXvCRdw (Python告诉你上海有哪些高性价比的西餐厅)
"""

import uniout
import time
import json
import io, os, sys

import numpy as np
import pandas as pd
from sklearn import preprocessing
from utils.my_logger import UtilLogger
from crawl.html_parser import get_restaurant_details
log = UtilLogger(os.path.basename(__file__), os.path.join("./log", os.path.basename(__file__).replace("py", "log")))
reload(sys)
sys.setdefaultencoding('utf-8')


def get_score(restaurant_df_, feat_col_):
    feat_weigh_ = np.array([float(ii)/sum(feat_col_.values()) for ii in feat_col_.values()])
    data_feat_df = restaurant_df_.loc[:, feat_col_.keys()].fillna(restaurant_df_.mean())  # 均值替换缺失值
    feat_scale_ = preprocessing.StandardScaler()
    feat_scale_result_ = feat_scale_.fit_transform(data_feat_df) * feat_weigh_
    feat_score_ = np.sum(feat_scale_result_, axis=1)  # 仅针对列
    min_ = min(feat_score_)
    max_ = max(feat_score_)
    feat_score_end_ = np.round((feat_score_ - min_) / (max_ - min_) * 100, 3)    # 百分制
    return feat_score_end_


def city_restaurant_main(city_key="beijing"):
    """
    获取某城市美食信息
    :param city_key:
    :return:
    """
    city_key = city_key.decode("utf-8")
    if u'\u4e00' <= city_key <= u'\u9fa5':
        from xpinyin import Pinyin
        p = Pinyin()
        city_tag_ = p.get_pinyin(city_key, '')
    else:
        city_tag_ = city_key
    with io.open(u"output/美食详情_{}.json".format(city_key), "w", encoding="utf-8") as fw:
        for ii in range(20):
            url = "http://www.dianping.com/{}/ch10/o4p{}".format(city_tag_, ii)
            page_result_ = get_restaurant_details(url)
            if page_result_ != -1:
                for line in page_result_:
                    line_str = json.dumps(line, encoding='UTF-8', ensure_ascii=False)
                    fw.write(line_str + "\n")
                log.info(u'城市: {}, 第{}页爬虫, 成功, 餐厅数量: {}'.format(city_key, ii, len(page_result_)))
            else:
                log.info(u'城市: {}, 第{}页爬虫, 失败'.format(city_key, ii))

    restaurant_df = pd.read_json(u"output/美食详情_{}.json".format(city_key), lines=True, encoding="utf-8").drop_duplicates()
    feature_col = {u"口味": 1.3, u"服务": 1.1, u"环境": 1.2, u"评论量": 0.5, u"星级标准": 1}

    restaurant_df[u"score"] = get_score(restaurant_df, feature_col)
    restaurant_end_df_ = restaurant_df.sort_values(by=["score"], ascending=False)
    try:
        restaurant_end_df_.to_csv(u"output/美食排行榜_{}.csv".format(city_key), index=False, encoding="gbk")
    except UnicodeEncodeError:
        restaurant_end_df_.to_csv(u"output/美食排行榜_{}.csv".format(city_key), index=False, encoding="utf-8")
    print(restaurant_end_df_.head())


if __name__ == '__main__':

    # city_list_ = [u"北京", u"敦煌", u"定州", u"格尔木", u"兰州", u"西宁", u"辛集", u"张掖"]
    city_list_ = [u"北京"]
    for city_ in city_list_:
        start = time.time()
        city_restaurant_main(city_)

        print("城市: {}, time: {:.2f}s".format(city_, time.time() - start))



