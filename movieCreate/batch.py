'''
批量生成视频
'''
from moviepy.editor import *
import re
from datetime import datetime
import getImgs
import os
from moviepy.video.fx import resize
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip

# 定义要处理的文件夹列表
input_folders = [ "input2", "input3","input4" ]  # 替换为实际的文件夹名称

# 循环遍历每个文件夹
for input_folder in input_folders:

    # Step 1: 加载音频和字幕文件
    # audio_path = 'yinpin.wav'
    # subtitle_path = 'zimu.srt'
    current_folder = os.path.dirname(os.path.abspath(__file__))
    audio_path = os.path.join(current_folder,input_folder, "yinpin.wav")
    subtitle_path = os.path.join(current_folder, input_folder, "zimu.srt")
    imgs_folder = os.path.join(current_folder, "imgs_folder")
    bgm_file = os.path.join(current_folder, "statics/rouhezhiguang-bgm.mp3")
    # bgm_file = os.path.join(current_folder, "rouhezhiguang-bgm.mp3")


    # 获取 imgs_folder 文件夹中所有文件和文件夹的列表
    file_list = os.listdir(imgs_folder)

    # 遍历列表，删除图片素材文件夹下面所有文件
    for file_name in file_list:
        file_path = os.path.join(imgs_folder, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


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


    subtitles = parse_subtitle(subtitle_path)

    # Step 3: 匹配表情包并生成视频片段 (示例函数)
    def get_emoticon_for_sentence(sentence):
        # 这里是示例函数，根据句子内容来选择对应的表情包
        # 实际应用中可能需要使用NLP技术或其他方法进行更准确的匹配
        image_urls = getImgs.get_image_urls(sentence)
        return image_urls[0]
        # return os.path.join(current_folder, "happy_emoticon.jpg")
    




    def create_video_segment(sentence, start_time_str, end_time_str, img_width, img_height, index):
        # 之前的代码保持不变
        time_format = "%H:%M:%S,%f"
        start_time = datetime.strptime(start_time_str, time_format)
        end_time = datetime.strptime(end_time_str, time_format)
            # 计算视频片段的时长（以秒为单位）
        duration = (end_time - start_time).total_seconds()

        # 将开始时间转换为相对于音频文件的起始时间的秒数
        audio_start_time = (start_time - datetime(1900, 1, 1)).total_seconds()

        duration = (end_time - start_time).total_seconds()
        if(index == 2): # 话题主题
            input_directory = os.path.join(current_folder, input_folder)
            netFriend_file_path = os.path.join(input_directory, "title.png")
            local_emoticon_path = netFriend_file_path
            img_width = 1600
            img_height = None
        # elif( "下面是来自网友的回复" in sentence ):
        elif( index == 3 or index == 4):   # 话题作者
            input_directory = os.path.join(current_folder, input_folder)
            netFriend_file_path = os.path.join(input_directory, "1.png")
            local_emoticon_path = netFriend_file_path
            img_width = 1500
            img_height = None

        else:
            emoticon_path = get_emoticon_for_sentence(sentence)
            local_emoticon_path = getImgs.download_image(emoticon_path, imgs_folder)

        if local_emoticon_path is not None:
            emoticon_clip = ImageClip(local_emoticon_path).set_duration(duration)

            # 设置图片大小
            emoticon_clip = resize(width=img_width, height=img_height) 
            # emoticon_clip = emoticon_clip.resize(width=img_width, height=img_height) 

            audio = AudioFileClip(audio_path).subclip(audio_start_time, audio_start_time + duration)
            # 设置图片位置为居中
            emoticon_clip = emoticon_clip.set_position(("center", "center"))
            emoticon_clip = emoticon_clip.set_audio(audio)


            # 创建一个大小为 1920x1080 的黑色背景视频
            background = ColorClip(size=(1920, 1080), color=(0, 0, 0)).set_duration(duration)

            # 将表情图片和音频剪辑合成到背景视频上
            # 计算图片在垂直方向上的偏移量
            if img_height is not None:
                video_clip = CompositeVideoClip([background, emoticon_clip.set_position(("center", 1080/2 - 400 -80)), ])

            else:
                # 如果img_height为None，使用默认的居中位置
                video_clip = CompositeVideoClip([background, emoticon_clip.set_position(("center", 'center')), ])





            # 叠加字幕剪辑和视频剪辑
            font_size = 60
            font_color = "white"
            subtitle_clip = TextClip(sentence, fontsize=font_size, color=font_color, font="STSong" )
            # 设置字幕的位置（固定在视频中心底部）
            subtitle_position = ("center", 1080 - 130)
            subtitle_clip = subtitle_clip.set_position(subtitle_position)
            # 将字幕剪辑设置为与视频相同的持续时间
            subtitle_clip = subtitle_clip.set_duration(duration)

            video_with_subtitle = CompositeVideoClip([video_clip, subtitle_clip])
        
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

        segment = create_video_segment(sentence, start_time, end_time, 1000, 800, index)
        video_segments.append(segment)

    # Step 5: 合并视频片段成最终视频
    final_video = concatenate_videoclips(video_segments, method="compose")



    # Step 6: 加上bgm


    # 从视频中提取音频
    video_audio = final_video.audio

    # 加载背景音乐
    bgm = AudioFileClip(bgm_file)

    # 调整背景音乐时长与视频一致
    bgm = bgm.set_duration(final_video.duration)

    # 将背景音乐叠加在视频的音频上
    final_audio = CompositeAudioClip([video_audio.volumex(1.0), bgm.volumex(0.4)])

    # 重新合成带有背景音乐的视频
    final_video_with_bgm = final_video.set_audio(final_audio)



    # # Step 7:导出最终视频
    # 定义要写入的文件夹路径（在当前目录下的output文件夹中）
    output_folder = os.path.join(current_folder, "output", f"{input_folder}.mp4")

    final_video_with_bgm.write_videofile(output_folder, codec="libx264", fps=30)




