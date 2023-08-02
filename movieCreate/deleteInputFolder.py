'''
Author: jiangxiaoyu
Date: 2023-08-01 22:41:06
LastEditors: jiangxiaoyu
LastEditTime: 2023-08-01 22:41:27
FilePath: /shengcai/movieCreate/deleteInputFolder.py
Description: 
'''
# 当前文件目录下同级下的所有的input_folders = ["input1", "input2", "input3","input4" ] 
# 这四个文件夹下面的文件进行清空

import os
import shutil

def clear_folders(folder_path):
    input_folders = ["input1", "input2", "input3", "input4"]

    for folder_name in input_folders:
        folder_dir = os.path.join(folder_path, folder_name)
        if not os.path.exists(folder_dir):
            continue

        for root, dirs, files in os.walk(folder_dir):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                
if __name__ == "__main__":
    current_directory = os.getcwd()
    clear_folders(current_directory)
