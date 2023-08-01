'''
Author: jiangxiaoyu
Date: 2023-07-27 15:46:44
LastEditors: jiangxiaoyu
LastEditTime: 2023-07-28 17:52:45
FilePath: /fengxiangbiao/getList copy.py
Description: 
'''
'''
Author: jiangxiaoyu
Date: 2023-07-27 15:46:44
LastEditors: jiangxiaoyu
LastEditTime: 2023-07-28 14:54:56
FilePath: /fengxiangbiao/getList copy.py
Description: 
'''
import requests
import writeMd
import constants
import re
import sys
import datetime

articleObj = {}
filename = 'result.md'

thisPageNotTheEnd = True


def getArticleList(page):

    # 获取今天的日期
    today = datetime.date.today()
    # 获取七天前的日期
    seven_days_ago = today - datetime.timedelta(days=1)
    # 将日期转换为datetime对象，并获取时间戳（以秒为单位）
    timestamp_today = str(int(datetime.datetime(today.year, today.month, today.day).timestamp()))
    timestamp_seven_days_ago = str(int(datetime.datetime(seven_days_ago.year, seven_days_ago.month, seven_days_ago.day).timestamp()))

    url = "https://i.shengcaiyoushu.com/search/article"
    headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Content-Type": "application/json",
    "Cookie": "__user_token.v3=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3Mzg1MDQsIm5hbWUiOiLpppnllrfllrfllabllabllaYiLCJ4cV9pZCI6MjE0Mzg2OCwibnVtYmVyIjo3NDI0MCwieHFfZ210X2V4cGlyZSI6MTcxMzM2OTYwMCwieHFfZ210X3VwZGF0ZSI6MTY4OTg0NjgxNH0.0UDjayVWsTRrHk3lcJ8YFJpSz-YhKQVuXvX2nkXVJs0",
    "Origin": "https://search01.shengcaiyoushu.com",
    "Pragma": "no-cache",
    "Referer": "https://search01.shengcaiyoushu.com/",
    "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"macOS\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "X-Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3Mzg1MDQsIm5hbWUiOiLpppnllrfllrfllabllabllaYiLCJ4cV9pZCI6MjE0Mzg2OCwibnVtYmVyIjo3NDI0MCwieHFfZ210X2V4cGlyZSI6MTcxMzM2OTYwMCwieHFfZ210X3VwZGF0ZSI6MTY4ODQzOTk1NH0.rrhywiFGwbH0w2aS7YsYdbh7WowWhvbWAGtpf9QWzvQ"
    }
    payload = {
        "form": {
            "menu_ids": ["21272"],
            "gmt_create":[timestamp_seven_days_ago, timestamp_today],
        },
        "orderBy": "score",
        "page": page,
        "keyword": "",
        "is_group_count": False
    }

    # payload ={"form":{"gmt_create":["1690473600","1690473600"],"menu_ids":["21272"]},"orderBy":"score","page":1,"keyword":"",  "is_group_count": False}
    
    response = requests.post(url, json=payload, headers=headers)
    
    return response.text  # 返回解析后的JSON数据

def getArticleInfo(topic_id):
    url = f"https://api.zsxq.com/v2/topics/{topic_id}/info"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Cookie": "zsxq_access_token=C4E06498-9C45-A27A-911E-161CC14472B3_BEC646A8DE728AD3; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22244145428481421%22%2C%22first_id%22%3A%2218606d481e88eb-00a7ca98a8714a-16525635-1296000-18606d481e99e6%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fsearch01.shengcaiyoushu.com%2F%22%7D%2C%22%24device_id%22%3A%2218606d481e88eb-00a7ca98a8714a-16525635-1296000-18606d481e99e6%22%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg3N2ZmNDI0MmI2NDEtMDY2YWU5OTg3OWVjYzE4LTFkNTI1NjM0LTEyOTYwMDAtMTg3N2ZmNDI0MmMxMDMwIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMjQ0MTQ1NDI4NDgxNDIxIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22244145428481421%22%7D%7D; zsxqsessionid=ab9e43a3ceb54f648da1f7c929f96218",
        "Origin": "https://wx.zsxq.com",
        "Pragma": "no-cache",
        "Referer": "https://wx.zsxq.com/",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "X-Request-Id": "9325c8293-f6ce-b2c0-872d-9fdf4b0d8be",
        "X-Signature": "43e643cc517561f8c9f7b86c0815cc6493bd3a8f",
        "X-Timestamp": "1690442662",
        "X-Version": "2.40.0"
    }


    # 获取返回值中的一部分用于第二个函数的请求参数（示例中以response_data.get()方法获取）
    payload = {
        # 使用第一个函数的返回值中的某个字段作为参数
        "topic_id": topic_id
    }

    response = requests.get(url, headers=headers, params=payload)
    return response.json()  # 返回解析后的JSON数据





def main(page):

    # 首先调用getArticleList函数
    articleListStr = (getArticleList(page))
    # 将字符串中的null替换为Python中的None
    articleListStr = articleListStr.replace('null', 'None')

    articleList = eval(articleListStr)

    if len(articleList["data"]["items"]) > 0:
        thisPageNotTheEnd = True
    else: 
        thisPageNotTheEnd = False

    # 遍历数组中的项目
    for item in articleList["data"]["items"]:

        topic_id = item["topic_id"]
        # print("Topic ID:", topic_id, item)
        # 使用获取到的topic_id调用getArticleInfo函数，并打印结果
        result = getArticleInfo(topic_id)
        # 获取talk中的images和text
        # talk_images = result["resp_data"]["topic"]["talk"]["images"]
        resp_data = result.get("resp_data", {})
        topic = resp_data.get("topic", {})
        talk = topic.get("talk", {})
        talk_text = talk.get("text", None)

        if  isinstance(talk_text, str):
            # 使用正则表达式匹配并去除整个标签
            pattern = r'<e type="(.*?)" hid="(.*?)" title="(.*?)" />'
            talk_text = re.sub(pattern, '', talk_text)


            images_list = talk.get("images", [])


            # 创建一个空列表，用于存储所有图片的大图URL
            imgList = []

            # 遍历所有图片，提取"large"中的URL并添加到imgList中
            for image in images_list:
                large_url = image["large"]["url"]
                imgList.append(large_url)

            # 创建articleContent字典，并将imgList和talk_text放入其中
            articleContent = {
                "imgList": imgList,
                "text": talk_text
            }

            # 初始化标题和标签
            title = None
            tags_list = []

            # 遍历tags数组
            for tag in constants.tags:
                # 如果talk_text中包含该tag
                if talk_text and isinstance(talk_text, str) and tag in talk_text:
                    # 如果还未设置标题，则将该tag作为标题
                    if not title:
                        title = tag
                    else:
                        # 否则将tag作为标签添加到标签列表中
                        tags_list.append(tag)
            # 如果title仍然为None，则将其设置为'其他'
            if title is None:
                title = '其他'


            # 将标题和标签添加到articleContent对象中
            articleContent["type"] = title
            articleContent["title"] = ""
            articleContent["tags"] = tags_list


            # 首先，检查 articleContent["type"] 是否在 articleObj 中作为键已经定义
            if articleContent["type"] in articleObj:
                # 如果已经定义，将 articleContent 添加到对应的列表中
                articleObj[articleContent["type"]] = [*articleObj[articleContent["type"]], articleContent]
            else:
                # 如果未定义，创建一个新的列表，并将 articleContent 添加到列表中
                articleObj[articleContent["type"]] = [articleContent]
        
    if thisPageNotTheEnd:
        main(page+1)



main(1)


# 遍历对象，将每个一级属性的值作为一个数组，并打印每个一级属性的key
for key, value in articleObj.items():
    print(f"分类： {key}")

    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"# {key}\n")  # 写入分类

    articleList = value
    # 遍历数组，打印每个元素的title
    # for articleContent in articleList:
    for index, articleContent in enumerate(articleList):
        writeMd.write_md_content(filename, f"{articleContent['type']} No{index+1}", articleContent['text'], articleContent['imgList'],  articleContent["tags"] )




