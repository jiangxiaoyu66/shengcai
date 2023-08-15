'''
下载所有图片,根据字幕文件去下载txt中选择好的文件
'''
from moviepy.editor import *
import re
from datetime import datetime
import getImgs
import os
from moviepy.video.fx import resize
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
from PIL import Image
import numpy as np
import cv2



input_folders = ["multiple1", ]  # 替换为实际的文件夹名称
current_folder = os.path.dirname(os.path.abspath(__file__))
imgs_folder = os.path.join(current_folder, "imgs_folder")




def is_png_image(file_path):
    try:
        img = Image.open(file_path)
        return img.format == "PNG"
    except Exception as e:
        return False



    

# Step 2: 解析字幕文件
def parse_subtitle(subtitle_path):
    subtitles = []  # 用于存储字幕的列表
    # 使用 'utf-8-sig' 编码会自动去除开头的 BOM，这样你的字幕文件内容就不会包含 \ufeff 了。
    with open(subtitle_path, 'r', encoding='utf-8-sig') as file:  
        lines = file.readlines()
        
        # 逐行读取SRT文件内容并处理
        index = None
        start_time = None
        end_time = None
        sentence = ""
        for line in lines:
            line = line.strip()
            if line.isdigit():
                if index is not None and start_time is not None and end_time is not None and sentence != "":
                    subtitles.append({'index': index, 'start_time': start_time, 'end_time': end_time, 'sentence': sentence})
                index = int(line)
                sentence = ""
            elif ' --> ' in line:
                start_time, end_time = line.split(' --> ')
            elif line != "":
                sentence += line + "\n"

        # 处理最后一条字幕
        if index is not None and start_time is not None and end_time is not None and sentence != "":
            subtitles.append({'index': index, 'start_time': start_time, 'end_time': end_time, 'sentence': sentence})

    return subtitles



# Step 3: 匹配表情包并生成视频片段 (示例函数)
def get_emoticon_for_sentence(sentence):
    # 这里是示例函数，根据句子内容来选择对应的表情包
    # 实际应用中可能需要使用NLP技术或其他方法进行更准确的匹配
    image_urls = getImgs.get_image_urls(sentence)

    index = 0
    downloadImg(image_urls, index, sentence)

    # return image_urls
    # return os.path.join(current_folder, "happy_emoticon.jpg")



def downloadImg(image_urls,index, sentence):
    # imgIsOk = getImgs.getImgIsOk(image_urls[index])
    # if imgIsOk:
    #     getImgs.download_image(image_urls[index], imgs_folder, sentence)
    # else:
    #     downloadImg(image_urls,index+1)
    getImgs.download_image(image_urls[index], imgs_folder, sentence)




# Step 4: 遍历字幕并下载图片
def process_subtitles(subtitles, imgs_folder):
    for subtitle in subtitles:
        sentence = subtitle['sentence'].strip()  # 获取句子内容
        duration = (datetime.strptime(subtitle['end_time'], '%H:%M:%S,%f') - datetime.strptime(subtitle['start_time'], '%H:%M:%S,%f')).total_seconds()  # 计算字幕显示时间
        
        # 获取对应的表情包视频片段
        get_emoticon_for_sentence(sentence)
        
        # 可以将视频片段保存起来，如果需要的话
        # emoticon_clip.write_videofile(os.path.join(imgs_folder, f"{sentence}.mp4"), codec='libx264')
        
        # 输出提示信息
        print(f"句子: {sentence}，下载表情包成功！")

# Step 5: 主函数，遍历所有文件夹并执行操作
def main():
    
    for input_folder in input_folders:
        subtitle_path = os.path.join(current_folder, input_folder, "今日话题.srt")
        # 解析字幕文件
        subtitles = parse_subtitle(subtitle_path)
        
        # 遍历字幕并下载图片
        process_subtitles(subtitles, imgs_folder)

if __name__ == "__main__":
    main()

