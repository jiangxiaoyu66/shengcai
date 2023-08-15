'''
Author: jiangxiaoyu
Date: 2023-08-13 17:25:51
LastEditors: jiangxiaoyu
LastEditTime: 2023-08-14 15:43:43
FilePath: /shengcai/movieCreate/chooseImgs copy.py
Description: 
'''
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import getImgs
from concurrent.futures import ThreadPoolExecutor
import re
from moviepy.editor import *
import re
from datetime import datetime
import getImgs
import os

current_folder = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(current_folder, 'img-sentence-list.txt')

class ImageSubtitleApp:
    def __init__(self, root, srt_file, max_images_per_row, total_images):
        self.root = root
        self.srt_file = srt_file
        self.max_images_per_row = max_images_per_row
        self.total_images = total_images
        self.subtitles = []
        self.current_subtitle_index = 0
        self.image_urls = []
        self.selected_images = []

        self.executor = ThreadPoolExecutor(max_workers=20)

        self.load_subtitles()
        self.load_and_show_subtitle()

    def load_subtitles(self):
        with open(self.srt_file, 'r', encoding='utf-8') as file:
            srt_content = file.read()

        self.subtitles = re.findall(r'\d+\n(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)\n(.+?)\n\n', srt_content, re.DOTALL)

    def load_and_show_subtitle(self):
        self.image_urls = getImgs.get_image_urls(self.subtitles[self.current_subtitle_index][2])[:self.total_images]
        self.selected_images = [False] * self.total_images

        subtitle_text = self.subtitles[self.current_subtitle_index][2]

        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.destroy()
        self.subtitle_label = tk.Label(self.root, text=subtitle_text, wraplength=800, justify='center')
        self.subtitle_label.pack(pady=20)

        self.load_and_show_images()

    def load_and_show_images(self):
        if hasattr(self, 'image_frame'):
            self.image_frame.destroy()
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack()

        for i, image_url in enumerate(self.image_urls):
            self.executor.submit(self.load_and_show_single_image, i, image_url)

    def load_and_show_single_image(self, index, image_url):
        response = requests.get(image_url)
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        image = image.resize((100, 100), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(self.image_frame, image=photo)
        label.image = photo

        row = index // self.max_images_per_row
        col = index % self.max_images_per_row

        label.grid(row=row, column=col, padx=10, pady=10)
        label.bind("<Button-1>", lambda event, idx=index: self.select_image(idx))

    def select_image(self, index):
        self.selected_images[index] = not self.selected_images[index]
        if self.selected_images[index]:
            self.image_frame.grid_slaves(row=index // self.max_images_per_row, column=index % self.max_images_per_row)[0].config(borderwidth=5, relief="solid")
        else:
            self.image_frame.grid_slaves(row=index // self.max_images_per_row, column=index % self.max_images_per_row)[0].config(borderwidth=0, relief="flat")
        self.write_to_statistics()
        self.next_subtitle()

    def write_to_statistics(self):
        selected_images_info = []

        for i, selected in enumerate(self.selected_images):
            if selected:
                selected_images_info.append(f"字幕: {self.subtitles[self.current_subtitle_index][2]}, 选中的图片链接: {self.image_urls[i]}")

        with open(filepath, "a", encoding="utf-8") as file:
            for info in selected_images_info:
                file.write(info + "\n")

    def next_subtitle(self):
        self.current_subtitle_index = (self.current_subtitle_index + 1) % len(self.subtitles)
        self.load_and_show_subtitle()

    def pre_subtitle(self):
        self.current_subtitle_index = (self.current_subtitle_index - 1) % len(self.subtitles)
        self.load_and_show_subtitle()

    def run(self):
        pre_button = tk.Button(self.root, text="上一句", command=self.pre_subtitle)
        pre_button.pack(pady=10)
        next_button = tk.Button(self.root, text="下一句", command=self.next_subtitle)
        next_button.pack(pady=10)

        self.root.mainloop()

if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(__file__))
    srt_file = os.path.join(current_folder, "multiple1", "今日话题.srt")
    
    max_images_per_row = 8
    total_images = 40

    root = tk.Tk()
    root.geometry("800x600")
    app = ImageSubtitleApp(root, srt_file, max_images_per_row, total_images)
    app.run()
