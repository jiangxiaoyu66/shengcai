'''
Author: jiangxiaoyu
Date: 2023-08-01 22:39:43
LastEditors: jiangxiaoyu
LastEditTime: 2023-08-01 22:40:49
FilePath: /shengcai/movieCreate/rename.py
Description: 
'''
# 用python

# 把当前文件目录下同级下的所有的input_folders = ["input1", "input2", "input3","input4" ] 
# 这四个文件夹下面的文件进行重命名

# 重命名的规则：
# 第一个png重命名为title.png
# 第2个png重命名为1.png
# wav文件重命名为yinpin.wav
# srt文件重命名为zimu.srt


# ChatGPT



import os

def rename_files(folder_path):
    input_folders = ["input1", "input2", "input3", "input4"]

    for folder_name in input_folders:
        folder_dir = os.path.join(folder_path, folder_name)
        if not os.path.exists(folder_dir):
            continue

        file_list = os.listdir(folder_dir)
        png_count = 0

        for file_name in file_list:
            file_path = os.path.join(folder_dir, file_name)

            if file_name.endswith(".png"):
                png_count += 1
                if png_count == 1:
                    new_name = "title.png"
                else:
                    new_name = f"{png_count - 1}.png"
            elif file_name.endswith(".wav"):
                new_name = "yinpin.wav"
            elif file_name.endswith(".srt"):
                new_name = "zimu.srt"
            else:
                continue

            new_path = os.path.join(folder_dir, new_name)
            os.rename(file_path, new_path)

if __name__ == "__main__":
    current_directory = os.getcwd()
    rename_files(current_directory)
