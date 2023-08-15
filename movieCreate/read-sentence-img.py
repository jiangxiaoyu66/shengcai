import os
import getImgs


current_folder = os.path.dirname(os.path.abspath(__file__))
imgs_folder = os.path.join(current_folder, "imgs_folder")

def read_and_parse_data():
    # 读取文件内容
    current_folder = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_folder, 'img-sentence-list.txt')

    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    # 初始化数据数组
    data = []

    # 按行分割文件内容
    lines = content.split('\n')

    # 遍历每行内容，提取字幕和图片链接
    for line in lines:
        if line.strip():
            parts = line.split(', ')
            subtitle = parts[0].split(': ')[1]
            image_link = parts[1].split(': ')[1]
            data.append({"字幕": subtitle, "图片链接": image_link})

    return data

if __name__ == "__main__":
    data = read_and_parse_data()

    # 输出整理后的数据
    for entry in data:
        sentence = entry["字幕"]
        image_url = entry["图片链接"]
        getImgs.download_image(image_url, imgs_folder, sentence)

