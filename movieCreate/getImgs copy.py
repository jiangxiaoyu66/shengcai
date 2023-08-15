import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import getImgs
from concurrent.futures import ThreadPoolExecutor

class ImageSelectorApp:
    def __init__(self, root, image_urls):
        self.root = root
        self.image_urls = image_urls
        self.selected_images = []

        self.canvas = tk.Canvas(root)
        self.canvas.pack()

        self.executor = ThreadPoolExecutor(max_workers=8)  # 根据需要设置最大线程数

        self.load_and_show_images()

    def load_and_show_images(self):
        images_per_row = 8
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

        col = index % 8
        row = index // 8

        label.grid(row=row, column=col, padx=10, pady=10)
        label.bind("<Button-1>", lambda event, idx=index: self.select_image(idx))

        self.selected_images.append(False)

    def select_image(self, index):
        self.selected_images[index] = not self.selected_images[index]
        if self.selected_images[index]:
            self.canvas.grid_slaves(row=index // 8, column=index % 8)[0].config(borderwidth=5, relief="solid")
            selected_image_url = self.image_urls[index]
            print("选择的图片链接：", selected_image_url)
        else:
            self.canvas.grid_slaves(row=index // 8, column=index % 8)[0].config(borderwidth=0, relief="flat")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    image_urls = getImgs.get_image_urls("我爱你")[:20]

    root = tk.Tk()
    root.geometry("1000x600")
    app = ImageSelectorApp(root, image_urls)
    app.run()
