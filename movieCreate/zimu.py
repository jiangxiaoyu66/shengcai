# -*- coding: utf-8 -*-
from moviepy.editor import *

def create_subtitle_video():
    # # 创建一个纯黑色背景的视频
    # duration = 10  # 视频时长为10秒
    # video_width, video_height = 1920, 1080  # 假设视频宽高为 1920x1080

    # size = (video_width, video_height)  # 视频尺寸
    # bg_color = (0, 0, 0)  # 黑色背景
    # video_clip = ColorClip(size, color=bg_color, duration=duration)
    fps = 30  # 帧率为每秒30帧
    video_width, video_height = 1920, 1080  # 假设视频宽高为 1920x1080

    current_folder = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(current_folder, "final_output.mp4")


    video_clip = VideoFileClip(video_path)
    duration = video_clip.duration  # 字幕显示的时间与视频时长一致
    

    # 定义字幕文本和样式
    subtitle_text = "这是一个固定字幕示例"
    font_size = 50
    font_color = "white"


    # 创建字幕文本剪辑
    font_path = "1689383973173053.ttf"
    subtitle_clip = TextClip(subtitle_text, fontsize=font_size, color=font_color, font="STSong" )

    # print(TextClip.list('font'))




    # 设置字幕的位置（固定在视频中心底部）
    subtitle_position = ("center", video_height )
    subtitle_clip = subtitle_clip.set_position(subtitle_position)

    # 将字幕剪辑设置为与视频相同的持续时间
    subtitle_clip = subtitle_clip.set_duration(duration)

    # 叠加字幕剪辑和视频剪辑
    video_with_subtitle = CompositeVideoClip([video_clip, subtitle_clip])

    # 保存生成的视频
    output_video_path = "aa.mp4"
    video_with_subtitle.write_videofile(output_video_path, codec="libx264", fps=fps)

    # 关闭视频剪辑和字幕剪辑
    video_clip.close()
    subtitle_clip.close()




    

if __name__ == "__main__":
    create_subtitle_video()



