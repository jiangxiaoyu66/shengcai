'''
Author: jiangxiaoyu
Date: 2023-08-13 17:25:51
LastEditors: jiangxiaoyu
LastEditTime: 2023-08-14 10:58:54
FilePath: /shengcai/movieCreate/getImgs copy 2.py
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



class ImageSubtitleApp:
    def __init__(self, root, srt_file):
        self.root = root
        self.srt_file = srt_file
        self.subtitles = []
        self.current_subtitle_index = 0
        self.image_urls = []
        self.selected_images = []

        self.canvas = tk.Canvas(root)
        self.canvas.pack()

        self.executor = ThreadPoolExecutor(max_workers=8)

        self.load_subtitles()
        self.load_and_show_subtitle()

    def load_subtitles(self):
        with open(self.srt_file, 'r', encoding='utf-8') as file:
            srt_content = file.read()

        self.subtitles = re.findall(r'\d+\n(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)\n(.+?)\n\n', srt_content, re.DOTALL)

    def load_and_show_subtitle(self):
        self.image_urls = getImgs.get_image_urls(self.subtitles[self.current_subtitle_index][2])[:20]
        self.selected_images = [False] * 20

        subtitle_text = self.subtitles[self.current_subtitle_index][2]

        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.destroy()
        self.subtitle_label = tk.Label(self.root, text=subtitle_text, wraplength=400, justify='left')
        self.subtitle_label.pack(side='left', padx=10, pady=10)

        self.load_and_show_images()

    def load_and_show_images(self):
        if hasattr(self, 'canvas'):
            self.canvas.destroy()
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(side='right', padx=10, pady=10)

        images_per_row = 4
        current_row = 0

        for i, image_url in enumerate(self.image_urls):
            self.executor.submit(self.load_and_show_single_image, i, image_url)

    def load_and_show_single_image(self, index, image_url):
        response = requests.get(image_url)
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        image = image.resize((100, 100), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(self.canvas, image=photo)
        label.image = photo

        col = index % 4
        row = index // 4

        label.grid(row=row, column=col, padx=10, pady=10)
        label.bind("<Button-1>", lambda event, idx=index: self.select_image(idx))

    def select_image(self, index):
        self.selected_images[index] = not self.selected_images[index]
        if self.selected_images[index]:
            self.canvas.grid_slaves(row=index // 4, column=index % 4)[0].config(borderwidth=5, relief="solid")
        else:
            self.canvas.grid_slaves(row=index // 4, column=index % 4)[0].config(borderwidth=0, relief="flat")
        app.next_subtitle()



    def next_subtitle(self):
        self.current_subtitle_index = (self.current_subtitle_index + 1) % len(self.subtitles)
        self.load_and_show_subtitle()
    
    def pre_subtitle(self):
        self.current_subtitle_index = (self.current_subtitle_index - 1) % len(self.subtitles)
        self.load_and_show_subtitle()


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(__file__))

    srt_file = os.path.join(current_folder, "multiple1", "今日话题.srt")


    root = tk.Tk()
    root.geometry("800x600")
    app = ImageSubtitleApp(root, srt_file)

  

    pre_button = tk.Button(root, text="上一句", command=app.pre_subtitle)
    pre_button.pack(pady=10)
    next_button = tk.Button(root, text="下一句", command=app.next_subtitle)
    next_button.pack(pady=10)

    app.run()
