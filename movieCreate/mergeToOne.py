# '''
# Author: jiangxiaoyu
# Date: 2023-08-09 09:56:28
# LastEditors: jiangxiaoyu
# LastEditTime: 2023-08-14 22:38:19
# FilePath: /shengcai/movieCreate/mergeToOne.py
# Description: 
# '''
# from moviepy.editor import VideoFileClip, concatenate_videoclips
# import os
# from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip

# # 指定子目录名
# current_folder = os.path.dirname(os.path.abspath(__file__))
# subdirectory_folder = os.path.join(current_folder, "output")
# bgm_file = os.path.join(current_folder, "statics/rouhezhiguang-bgm.mp3")

# # 获取子目录中所有的视频文件
# video_files = [os.path.join(subdirectory_folder, file) for file in os.listdir(subdirectory_folder) if file.endswith('.mp4') and os.path.isfile(os.path.join(subdirectory_folder, file))]

# # 按文件名排序视频文件列表
# video_files.sort()

# # 创建VideoFileClip对象列表
# video_clips = [VideoFileClip(file) for file in video_files]

# # 合并视频
# final_clip = concatenate_videoclips(video_clips)


# # 从视频中提取音频
# video_audio = final_clip.audio

# # 加载背景音乐
# bgm = AudioFileClip(bgm_file)
# # 调整背景音乐时长与视频一致
# bgm = bgm.set_duration(final_clip.duration)
# # 将背景音乐叠加在视频的音频上
# final_audio = CompositeAudioClip([video_audio.volumex(1.0), bgm.volumex(0.3)])
# # 重新合成带有背景音乐的视频
# final_video_with_bgm = final_clip.set_audio(final_audio)


# # 保存合并后的视频
# output_filename = subdirectory_folder
# final_video_with_bgm.write_videofile(os.path.join(output_filename, 'mergedVideo.mp4'), codec='libx264')

# # 关闭VideoFileClip对象
# for clip in video_clips:
#     clip.close()

# # 关闭合并后的视频对象
# final_clip.close()












from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
import os

# 指定子目录名
current_folder = os.path.dirname(os.path.abspath(__file__))
subdirectory_folder = os.path.join(current_folder, "output")
bgm_file = os.path.join(current_folder, "statics/rouhezhiguang-bgm.mp3")

# 获取子目录中所有的视频文件
video_files = [os.path.join(subdirectory_folder, file) for file in os.listdir(subdirectory_folder) if file.endswith('.mp4') and os.path.isfile(os.path.join(subdirectory_folder, file))]

# 按文件名排序视频文件列表
video_files.sort()

# 创建VideoFileClip对象列表
video_clips = [VideoFileClip(file) for file in video_files]

# 合并视频
final_clip = concatenate_videoclips(video_clips)

# 从视频中提取音频
video_audio = final_clip.audio

# 加载背景音乐
bgm = AudioFileClip(bgm_file)
bgm_duration = bgm.duration

# 调整背景音乐时长与视频一致，并循环播放音频
if bgm_duration < final_clip.duration:
    # 计算需要循环播放的次数
    loop_count = int(final_clip.duration / bgm_duration)
    # 重复背景音乐片段并拼接
    bgm = CompositeAudioClip([bgm] * (loop_count))
    # 将剩余时间的音频添加到背景音乐
    bgm = CompositeAudioClip([bgm, bgm.subclip(0, final_clip.duration % bgm_duration)])
else:
    # 调整背景音乐时长与视频一致
    bgm = bgm.set_duration(final_clip.duration)

# 将背景音乐叠加在视频的音频上
final_audio = CompositeAudioClip([video_audio.volumex(1.0), bgm.volumex(0.3)])

# 重新合成带有背景音乐的视频
final_video_with_bgm = final_clip.set_audio(final_audio)

# 保存合并后的视频
output_filename = subdirectory_folder
final_video_with_bgm.write_videofile(os.path.join(output_filename, 'mergedVideo.mp4'), codec='libx264')

# 关闭VideoFileClip对象
for clip in video_clips:
    clip.close()

# 关闭合并后的视频对象
final_clip.close()
