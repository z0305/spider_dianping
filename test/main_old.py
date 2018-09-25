# -*- coding: utf-8 -*-
"""
__author__ = z0305
__date__ = 08/16/2018
__purpose__ =
__site__ = https://mp.weixin.qq.com/s/dkaV4VZ1QBzcsi9gXvCRdw (Python告诉你上海有哪些高性价比的西餐厅)
           https://github.com/pythonml/restaurant
"""
import re
import json
import pymongo
from lxml import etree
import requests
import pandas as pd
import matplotlib.pyplot as plt
from config import STRING_NUM

DB = "restaurant"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "www.dianping.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "Cookie": "cy=1; cye=shanghai; _lxsdk_cuid=1653dcc99a6c8-04ff4f92706bc4-1c2f1702-2f4f0c-1653dcc99a6bb; _lxsdk=1653dcc99a6c8-04ff4f92706bc4-1c2f1702-2f4f0c-1653dcc99a6bb; _hc.v=c668bd43-a103-53a2-3ccb-2d01ad06f352.1534340144; _lxsdk_s=1653dcc99ae-1-d99-0e5%7C%7C48",
}


def get_districts():
    url = "http://www.dianping.com/shanghai/ch10/g116"
    r = requests.get(url, headers=headers, verify=False)
    content = r.content.decode("utf-8")
    print("====")
    print(content)
    root = etree.HTML(content)
    distr_nodes = root.xpath('.//div[@id="region-nav"]')
    if len(distr_nodes) == 0:
        raise Exception("no districts")
    distr_node = distr_nodes[0]
    result = []
    for node in distr_node:
        name = node.attrib["data-click-title"]
        url = node.attrib["href"]
        result.append({"name": name, "url": url})
    return result


def get_sub_districts():
    districts = get_districts()
    client = pymongo.MongoClient()
    db = client[DB]
    for item in districts:
        distr_name = item["name"]
        distr_url = item["url"]
        r = requests.get(distr_url, headers=headers, verify=False)
        content = r.content.decode("utf-8")
        root = etree.HTML(content)
        sub_nodes = root.xpath('.//div[@id="region-nav-sub"]/a[@data-cat-id]')
        for node in sub_nodes:
            url = node.attrib["href"]
            name = node.xpath('./span')[0].text
            db.sub.insert_one({"district": distr_name, "sub": name, "url": url})


def get_restaurants_by_district(entry_url, sub_id):
    i = 1
    client = pymongo.MongoClient()
    db = client[DB]
    while True:
        if i > 50:
            print("{} has more than 50 pages".format(url))
            break

        url = "{}p{}".format(entry_url, i)
        print(url)
        r = requests.get(url, headers=headers, verify=False)
        content = r.content.decode("utf-8")
        root = etree.HTML(content)
        rest_nodes = root.xpath('.//div[@id="shop-all-list"]/ul/li')
        if len(rest_nodes) == 0:
            break
        for node in rest_nodes:
            a_nodes = node.xpath('.//div[@class="tit"]/a')
            if len(a_nodes) == 0:
                continue
            url = a_nodes[0].attrib["href"]
            name = a_nodes[0].attrib["title"]
            db.restaurant_url.insert_one({"name": name, "url": url, "sub_id": sub_id, "is_done": False})
        i += 1

def get_all_restaurants():
    client = pymongo.MongoClient()
    db = client[DB]
    sub_rows = db.sub.find()
    for row in sub_rows:
        district = row["district"]
        url = row["url"]
        sub_id = row["_id"]
        print(district)
        get_restaurants_by_district(url, sub_id)


def get_price(node):
    text = node.text
    matched = re.search(r"人均\D+(\d+)", text)
    price = 0
    if matched:
        price = int(matched.group(1))
    digit_nodes = node.xpath('./span')
    for digit_node in digit_nodes:
        span_class = digit_node.attrib["class"]
        num = STRING_NUM[span_class]
        price = price * 10 + num
        if digit_node.tail:
            matched = re.search(r"(\d+)", digit_node.tail)
            if matched:
                power = len(matched.group(1))
                price = price * 10**power + int(matched.group(1))
    return price


def get_score(node):
    digit_nodes = node.xpath('./span')
    score = 0
    text = node.text
    matched = re.search(r"(\d+)", text)
    if matched:
        score = matched.group(1)

    for digit_node in digit_nodes:
        span_class = digit_node.attrib["class"]
        num = STRING_NUM[span_class]
        score = score * 10 + num
        tail = digit_node.tail
        if tail is not None:
            matched = re.search(r"(\d+)", tail)
            if matched:
                score = score * 10 + int(matched.group(1))
    score = score / 10
    return score

def get_restaurant_details():
    client = pymongo.MongoClient()
    db = client[DB]
    rest_rows = db.restaurant_url.find({"is_done": False})
    done_urls = []
    for row in rest_rows:
        url = row["url"]
        #url = "http://www.dianping.com/shop/5735627"
        #url = "http://www.dianping.com/shop/69208935"
        #url = "http://www.dianping.com/shop/66183142"
        #url = "http://www.dianping.com/shop/13932333"
        if url in done_urls:
            continue
        sub_id = row["sub_id"]
        print(url)
        r = requests.get(url, headers=headers, verify=False)
        content = r.content.decode("utf-8")
        root = etree.HTML(content)
        info_nodes = root.xpath('.//div[@id="basic-info"]')
        if len(info_nodes) == 0:
            print("no info for {}".format(url))
            continue
        name = info_nodes[0].xpath('.//h1[@class="shop-name"]')[0].text
        review_count = 0
        star = 0
        price = 0
        taste_score = 0
        env_score = 0
        service_score = 0
        star_nodes = info_nodes[0].xpath('.//div[@class="brief-info"]/span[contains(@class, "mid-rank-stars")]')
        if len(star_nodes) > 0:
            star_class = star_nodes[0].attrib["class"]
            matched = re.search(r"mid-str(\d+)", star_class)
            if matched:
                star = int(matched.group(1))
        review_nodes = info_nodes[0].xpath('.//div[@class="brief-info"]/span[@id="reviewCount"]')
        if len(review_nodes) > 0:
            review_info = review_nodes[0].text
            matched = re.search(r"(\d+)条评论", review_info)
            if matched:
                review_count = int(matched.group(1))
        price_nodes = info_nodes[0].xpath('.//div[@class="brief-info"]/span[@id="avgPriceTitle"]')
        if len(price_nodes) > 0:
            price = get_price(price_nodes[0])
            print(price)
        comment_nodes = info_nodes[0].xpath('.//div[@class="brief-info"]/span[@id="comment_score"]')
        if len(comment_nodes) > 0:
            score_nodes = comment_nodes[0].xpath('./span')
            for score_node in score_nodes:
                if re.search(r"口味", score_node.text):
                    taste_score = get_score(score_node)
                if re.search(r"环境", score_node.text):
                    env_score = get_score(score_node)
                if re.search(r"服务", score_node.text):
                    service_score = get_score(score_node)
        db.restaurant.insert_one({"name": name,
            "star": star,
            "price": price,
            "review_count": review_count,
            "taste_score": taste_score,
            "env_score": env_score,
            "service_score": service_score,
            "url": url,
            "sub_id": sub_id
        })
        db.restaurant_url.update_many({"url": url}, {"$set": {"is_done": True}})
        done_urls.append(url)

def unique():
    client = pymongo.MongoClient()
    db = client[DB]
    urls = db.restaurant.distinct("url")
    for url in urls:
        row_count = db.restaurant.find({"url": url}).count()
        if row_count == 1:
            continue
        rows = db.restaurant.find({"url": url})
        i = 0
        for row in rows:
            if i == 0:
                i += 1
                continue
            db.restaurant.delete_one({"_id": row["_id"]})
            i += 1

def update_index():
    client = pymongo.MongoClient()
    db = client[DB]
    restaurants = db.restaurant.find({"review_count": {"$gt": 100}})
    for item in restaurants:
        taste_score = item["taste_score"]
        env_score = item["env_score"]
        service_score = item["service_score"]
        price = item["price"]
        if taste_score == 0 or env_score == 0 or service_score == 0:
            continue
        index = 3/(1/taste_score+1/env_score+1/service_score) / price * 1000
        avg_score = 3/(1/taste_score+1/env_score+1/service_score)
        db.restaurant.update({"_id": item["_id"]}, {"$set": {"index": index, "avg_score": avg_score}})

def stats():

    client = pymongo.MongoClient("172.24.176.73")
    db = client[DB]

    print("============ most expensive ===================")
    restaurants = db.restaurant.aggregate([
        {"$match": {"price": {"$gt": 0}}},
        {"$sort": {"price": 1}},
        {"$limit": 10},
    ])
    for item in restaurants:
        name = item["name"]
        review_count = item["review_count"]
        star = item["star"]
        price = item["price"]
        print("{},{}".format(name, price))

    print("============ highest index ===================")
    restaurants = db.restaurant.aggregate([
        {"$sort": {"index": -1}},
        {"$limit": 10}
    ])
    for item in restaurants:
        name = item["name"]
        review_count = item["review_count"]
        star = item["star"]
        price = item["price"]
        index = item["index"]
        taste_score = item["taste_score"]
        env_score = item["env_score"]
        service_score = item["service_score"]
        print("{},{},{},{},{},{}".format(name, price, taste_score, env_score, service_score, index))

    print("============ highest index > 100 ===================")
    restaurants = db.restaurant.aggregate([
        {"$match": {"price": {"$gt": 100}}},
        {"$sort": {"index": -1}},
        {"$limit": 10}
    ])
    for item in restaurants:
        name = item["name"]
        review_count = item["review_count"]
        star = item["star"]
        price = item["price"]
        index = item["index"]
        taste_score = item["taste_score"]
        env_score = item["env_score"]
        service_score = item["service_score"]
        print(name, price, review_count, taste_score, env_score, service_score, index)

    print("============ highest avg_score ===================")
    restaurants = db.restaurant.aggregate([
        {"$match": {"price": {"$gt": 200}}},
        {"$match": {"price": {"$lt": 300}}},
        {"$sort": {"index": -1}},
        {"$limit": 50}
    ])
    for item in restaurants:
        name = item["name"]
        review_count = item["review_count"]
        star = item["star"]
        price = item["price"]
        index = item["index"]
        taste_score = item["taste_score"]
        env_score = item["env_score"]
        service_score = item["service_score"]
        avg_score = item["avg_score"]
        print("{},{},{}".format(name, price, avg_score))

    #restaurants = db.restaurant.find({})
    #df = pd.DataFrame(columns=["price", "avg_score"])
    #for item in restaurants:
    #    df.loc[len(df)] = [item.get("price"), item.get("avg_score")]
    #print(df)
    #fig, ax = plt.subplots()
    #df.avg_score.hist(ax=ax, bins=20)
    #plt.show()

if __name__ == "__main__":
    stats()
