'''
Author: jiangxiaoyu
Date: 2023-07-31 13:42:24
LastEditors: jiangxiaoyu
LastEditTime: 2023-07-31 21:41:01
FilePath: /shengcai/movieCreate/index copy.py
Description: 
'''
from moviepy.editor import *
import re
from datetime import datetime
import getImgs
from moviepy.video.fx import resize


# Step 1: 加载音频和字幕文件
# audio_path = 'yinpin.wav'
# subtitle_path = 'zimu.srt'
current_folder = os.path.dirname(os.path.abspath(__file__))
audio_path = os.path.join(current_folder, "yinpin.wav")
subtitle_path = os.path.join(current_folder, "zimu.srt")
imgs_folder = os.path.join(current_folder, "imgs_folder")
bgm_path = os.path.join(current_folder, "rouhezhiguang-bgm.mp3")


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
    image_urls = getImgs.get_image_urls(sentence)
    return image_urls[0]
    # return os.path.join(current_folder, "happy_emoticon.jpg")
  




def create_video_segment(sentence, start_time_str, end_time_str, img_width, img_height):
    # 之前的代码保持不变
    time_format = "%H:%M:%S,%f"
    start_time = datetime.strptime(start_time_str, time_format)
    end_time = datetime.strptime(end_time_str, time_format)
        # 计算视频片段的时长（以秒为单位）
    duration = (end_time - start_time).total_seconds()

    # 将开始时间转换为相对于音频文件的起始时间的秒数
    audio_start_time = (start_time - datetime(1900, 1, 1)).total_seconds()

    duration = (end_time - start_time).total_seconds()
    emoticon_path = get_emoticon_for_sentence(sentence)
    local_emoticon_path = getImgs.download_image(emoticon_path, imgs_folder)

    if local_emoticon_path is not None:
        emoticon_clip = ImageClip(local_emoticon_path).set_duration(duration)

        # 设置图片大小
        emoticon_clip = emoticon_clip.resize(width=img_width, height=img_height) 

        audio = AudioFileClip(audio_path).subclip(audio_start_time, audio_start_time + duration)

        # 加上bgm
        bgm_audio = AudioFileClip(bgm_path)
        audio = audio.set_audio(bgm_audio)


        # 设置图片位置为居中
        emoticon_clip = emoticon_clip.set_position(("center", "center"))
        emoticon_clip = emoticon_clip.set_audio(audio)


        # 创建一个大小为 1920x1080 的黑色背景视频
        background = ColorClip(size=(1920, 1080), color=(0, 0, 0)).set_duration(duration)

        # 将表情图片和音频剪辑合成到背景视频上
        video_clip = CompositeVideoClip([background, emoticon_clip.set_position(("center", "center")), ])




        # 叠加字幕剪辑和视频剪辑
        font_size = 50
        font_color = "white"
        subtitle_clip = TextClip(sentence, fontsize=font_size, color=font_color, font="STSong" )
        # 设置字幕的位置（固定在视频中心底部）
        subtitle_position = ("center", 1080 - 60)
        subtitle_clip = subtitle_clip.set_position(subtitle_position)
         # 将字幕剪辑设置为与视频相同的持续时间
        subtitle_clip = subtitle_clip.set_duration(duration)

        video_with_subtitle = CompositeVideoClip([video_clip, subtitle_clip])
            # 保存生成的视频
        output_video_path = "aa.mp4"
        # video_with_subtitle.write_videofile(output_video_path, codec="libx264", fps=30)

        return video_with_subtitle
        # return video_clip
    else:
        return None




# def create_video_segment(sentence, start_time_str, end_time_str):
#     # 将时间字符串转换为时间类型
#     time_format = "%H:%M:%S,%f"
#     start_time = datetime.strptime(start_time_str, time_format)
#     end_time = datetime.strptime(end_time_str, time_format)

#     # 计算视频片段的时长（以秒为单位）
#     duration = (end_time - start_time).total_seconds()

#     # 将开始时间转换为相对于音频文件的起始时间的秒数
#     audio_start_time = (start_time - datetime(1900, 1, 1)).total_seconds()

#     emoticon_path = get_emoticon_for_sentence(sentence)

#     local_emoticon_path = getImgs.download_image(emoticon_path, imgs_folder)
#     if local_emoticon_path is not None:
#         emoticon_clip = ImageClip(local_emoticon_path).set_duration(duration)
#                 # 设置图片大小
#         emoticon_clip = emoticon_clip.fx(resize, width=1000, height=700)


#         audio = AudioFileClip(audio_path).subclip(audio_start_time, audio_start_time + duration)
#         emoticon_clip = emoticon_clip.set_audio(audio)
#         return emoticon_clip
#     else:
#         return None



    # emoticon_clip = ImageClip(emoticon_path).set_duration(duration)

    # audio = AudioFileClip(audio_path).subclip(audio_start_time, audio_start_time + duration)
    # emoticon_clip = emoticon_clip.set_audio(audio)
    # return emoticon_clip




# Step 4: 生成视频片段
video_segments = []
for subtitle in subtitles:
    index = subtitle['index']
    start_time = subtitle['start_time']
    end_time = subtitle['end_time']
    sentence = subtitle['sentence']

    segment = create_video_segment(sentence, start_time, end_time, 1000, 800)
    video_segments.append(segment)

# Step 5: 合并视频片段成最终视频
final_video = concatenate_videoclips(video_segments, method="compose")

# 导出最终视频
final_video.write_videofile("final_output.mp4", codec="libx264", fps=25)
