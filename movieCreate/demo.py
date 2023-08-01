'''
Author: jiangxiaoyu
Date: 2023-07-31 13:42:24
LastEditors: jiangxiaoyu
LastEditTime: 2023-07-31 14:34:23
FilePath: /shengcai/movieCreate/demo.py
Description: 
'''
from moviepy.editor import *
import moviepy
import re
from datetime import datetime
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip



# Step 1: 加载音频和字幕文件
# audio_path = 'yinpin.wav'
# subtitle_path = 'zimu.srt'
current_folder = os.path.dirname(os.path.abspath(__file__))
audio_path = os.path.join(current_folder, "yinpin.wav")
subtitle_path = os.path.join(current_folder, "zimu.srt")

# Step 2: 解析字幕文件
def parse_subtitle(subtitle_path):
    subtitles = []  # 用于存储字幕的列表
    with open(subtitle_path, 'r', encoding='utf-8') as file:
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


subtitles = parse_subtitle(subtitle_path)

# Step 3: 匹配表情包并生成视频片段 (示例函数)
def get_emoticon_for_sentence(sentence):
    # 这里是示例函数，根据句子内容来选择对应的表情包
    # 实际应用中可能需要使用NLP技术或其他方法进行更准确的匹配
  
        return os.path.join(current_folder, "happy_emoticon.jpg")
  

def create_video_segment(sentence, start_time_str, end_time_str):
    # 将时间字符串转换为时间类型
    time_format = "%H:%M:%S,%f"
    start_time = datetime.strptime(start_time_str, time_format)
    end_time = datetime.strptime(end_time_str, time_format)

    # 计算视频片段的时长（以秒为单位）
    duration = (end_time - start_time).total_seconds()

    # 将开始时间转换为相对于音频文件的起始时间的秒数
    audio_start_time = (start_time - datetime(1900, 1, 1)).total_seconds()


      # 获取表情包图片
    emoticon_path = get_emoticon_for_sentence(sentence)
    emoticon_clip = ImageClip(emoticon_path).set_duration(duration)

    # 创建字幕文本
    txt_clip = TextClip(sentence, fontsize=40, color='white', size=(emoticon_clip.w, None), align='center')

    # 设置字幕持续时间
    txt_clip = txt_clip.set_duration(duration)

    # 合并表情包和字幕
    video_with_subtitle = CompositeVideoClip([emoticon_clip, txt_clip.set_position(('center', 'bottom'))])

    # 合并音频和视频
    audio = AudioFileClip(audio_path).subclip(audio_start_time, audio_start_time + duration)
    video_with_subtitle = video_with_subtitle.set_audio(audio)

    return video_with_subtitle



# Step 4: 生成视频片段
video_segments = []
for subtitle in subtitles:
    index = subtitle['index']
    start_time = subtitle['start_time']
    end_time = subtitle['end_time']
    sentence = subtitle['sentence']

    segment = create_video_segment(sentence, start_time, end_time)
    video_segments.append(segment)


# Step 5: 合并视频片段成最终视频
final_video = concatenate_videoclips(video_segments, method="compose")

# 导出最终视频
final_video.write_videofile("final_output.mp4", codec="libx264", fps=25)
