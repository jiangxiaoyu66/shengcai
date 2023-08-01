'''
Author: jiangxiaoyu
Date: 2023-07-31 16:13:28
LastEditors: jiangxiaoyu
LastEditTime: 2023-07-31 17:00:06
FilePath: /shengcai/movieCreate/getImgs.py
Description: 
'''
import requests
from bs4 import BeautifulSoup
import os



def get_image_urls(keyword):
    base_url = "https://www.pkdoutu.com/search"
    params = {"keyword": keyword}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
    }

    response = requests.get(base_url, params=params, headers=headers, verify=False)
    # print(response.text)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        image_urls = []

        # 图片地址通常位于<img>标签的src属性中
        image_elements = soup.find_all("img")

        for img in image_elements:
            image_url = img.get("data-original")
            if image_url:
                # 将字符串中的旧URL替换为新URL
                image_url = image_url.replace("https://doutula-oss.oss-cn-hongkong.aliyuncs.com", "https://img.pkdoutu.com")
                image_urls.append(image_url)



        return image_urls
    else:
        print(f"请求失败：{response.status_code}")
        return []

# if __name__ == "__main__":
#     keyword = "目标就是考上大学"
#     image_urls = get_image_urls(keyword)
#     for url in image_urls:
#         print(url)


def download_image(image_url, save_folder):
    response = requests.get(image_url, verify=False)
    if response.status_code == 200:
        filename = os.path.basename(image_url)
        save_path = os.path.join(save_folder, filename)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return save_path
    else:
        print(f"下载图片失败：{response.status_code}")
        return None