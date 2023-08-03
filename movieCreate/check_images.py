'''
Author: jiangxiaoyu
Date: 2023-08-02 21:12:02
LastEditors: jiangxiaoyu
LastEditTime: 2023-08-02 21:21:22
FilePath: /shengcai/movieCreate/Untitled-1.py
Description: 
'''


from PIL import Image

import os

current_folder = os.path.dirname(os.path.abspath(__file__))

imgs_folder = os.path.join(current_folder, "imgs_folder")

def check_images(folder_path):
    # 获取文件夹中所有图片的文件名
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.gif')]

    if len(image_files) == 0:
        print("文件夹中没有图片。")
        return

    # 用于存储图片尺寸和颜色通道数
    image_sizes = set()
    color_channels = set()

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        try:
            # 打开图片
            image = Image.open(image_path)
            # 获取图片尺寸
            image_size = image.size
            # 获取图片颜色通道数
            num_channels = len(image.getbands())
            print('图片的数据类型',image_path, image.mode)

            # 添加到集合中
            image_sizes.add(image_size)
            color_channels.add(num_channels)

            # 关闭图片
            image.close()
        except Exception as e:
            print(f"处理图片 {image_file} 时出现错误: {e}")

        # 检查所有图片是否具有相同的尺寸和颜色通道数
        if len(image_sizes) == 1 and len(color_channels) == 1:
            print("所有图片的尺寸和颜色通道数都一致。")
            print(f"图片尺寸: {image_sizes.pop()}")
            print(f"颜色通道数: {color_channels.pop()}")
        else:
            
            
            print("图片的尺寸或颜色通道数不一致。", image_path)
            print(f"不同的图片尺寸: {image_sizes}")
            print(f"不同的颜色通道数: {color_channels}")


check_images(imgs_folder)


