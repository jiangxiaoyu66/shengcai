from moviepy.editor import VideoFileClip
import getImgs


# Step 3: 匹配表情包并生成视频片段 (示例函数)
def get_emoticon_for_sentence(sentence):
    # 这里是示例函数，根据句子内容来选择对应的表情包
    # 实际应用中可能需要使用NLP技术或其他方法进行更准确的匹配
    image_urls = getImgs.get_image_urls(sentence)
    return image_urls
    # return os.path.join(current_folder, "happy_emoticon.jpg")




def get_emoticon_clip(sentence, duration, imgs_folder):
    try:
        emoticon_path = get_emoticon_for_sentence(sentence)[1]
        local_emoticon_path = getImgs.download_image(emoticon_path, imgs_folder)
        emoticon_clip = VideoFileClip(local_emoticon_path).set_duration(duration)
        return emoticon_clip
    except Exception as e:
        emoticon_path = get_emoticon_for_sentence(sentence)[1]
        local_emoticon_path = getImgs.download_image(emoticon_path, imgs_folder)
        emoticon_clip = VideoFileClip(local_emoticon_path).set_duration(duration)
        try:
            emoticon_path = get_emoticon_for_sentence(sentence)[2]
            local_emoticon_path = getImgs.download_image(emoticon_path, imgs_folder)
            emoticon_clip = VideoFileClip(local_emoticon_path).set_duration(duration)
            return emoticon_clip
        except Exception as e:
            # 如果在获取表情包时出现异常，尝试使用默认表情包或其他方式来获取
            default_emoticon_path = 'path_to_default_emoticon.png'  # 替换为默认表情包的路径
            local_default_emoticon_path = getImgs.download_image(default_emoticon_path, imgs_folder)
            emoticon_clip = VideoFileClip(local_default_emoticon_path).set_duration(duration)
            return emoticon_clip

# 使用方式示例：
# 注意：您需要确保 get_emoticon_for_sentence 和 getImgs.download_image 这两个函数是正确定义并且可用的。

sentence = "这是一个测试句子"
duration = 5  # 表情包持续时长

emoticon_clip = get_emoticon_clip(sentence, duration, "path_to_imgs_folder")  # 替换为表情包图片存放的文件夹路径


