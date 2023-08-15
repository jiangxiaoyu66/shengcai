'''
Author: jiangxiaoyu
Date: 2023-07-31 16:13:28
LastEditors: jiangxiaoyu
LastEditTime: 2023-08-14 16:38:15
FilePath: /shengcai/movieCreate/getImgs.py
Description: 
'''
import requests
from bs4 import BeautifulSoup
import os
from io import BytesIO
from PIL import Image
from urllib.parse import urlparse



threshold_resolution=(200, 200)
threshold_size=90000
def getImgIsOk(image_url): 
    imgIsOk = True

    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        
        width, height = img.size
        file_size = width * height

        if width< height:
            imgIsOk = False
        
        if width >= threshold_resolution[0] and height >= threshold_resolution[1]:
            print("分辨率符合高清标准")
            imgIsOk = True
        else:
            imgIsOk = False
            print("分辨率较低")
        
        print('文件大小',file_size)
        if file_size >= threshold_size:
            print("文件大小符合高清标准")
            imgIsOk = True
        else:
            imgIsOk = False
            print("文件大小较小")

            
    except IOError:
        imgIsOk = False
        print("无法打开图片")

    return imgIsOk



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


# def download_image(image_url, save_folder, sentence):
#     response = requests.get(image_url, verify=False)
#     if response.status_code == 200:
#         # filename = os.path.basename(image_url)
#         # 获取图片的原始扩展名
#         parsed_url = urlparse(image_url)
#         image_extension = os.path.splitext(parsed_url.path)[-1]
        
#         # 使用句子作为文件名，并添加原始扩展名
#         filename = f"{sentence}{image_extension}"
#         save_path = os.path.join(save_folder, filename)
#         with open(save_path, 'wb') as f:
#             f.write(response.content)
#         return save_path
#     else:
#         print(f"下载图片失败：{response.status_code}")
#         return None
    

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