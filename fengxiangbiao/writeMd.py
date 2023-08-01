'''
Author: jiangxiaoyu
Date: 2023-07-27 15:28:17
LastEditors: jiangxiaoyu
LastEditTime: 2023-07-28 15:04:38
FilePath: /fengxiangbiao/writeMd.py
Description: 
'''

def write_md_content(filename, title, text, image_paths, tags):

    with open(filename, "a", encoding="utf-8") as file:


        file.write(f"## {title}\n")  # 写入标题
        file.write(f"{text}\n\n")   # 写入正文

        file.write(f"### 标签\n")  # 写入标题
        for i in range(len(tags)):
            file.write(f"{tags[i]},")  # 写入标题

        

        file.write(f"\n### 图片\n")  # 写入标题
        for i in range(len(image_paths)):
            image_path = image_paths[i]
            if image_path:
                # file.write(f"![图片描述]({image_path})\n\n")  # 写入图片
                file.write("<div style=\"width: 33%;display: inline-block \">\n")  # 设置每个图片所占宽度为三分之一
                file.write(f"  <img src=\"{image_path}\" alt=\"图片描述\">\n")  # 设置图片最大宽度为100%
                file.write("</div>\n")





# if __name__ == "__main__":
#     # 示例数据
#     md_filename = "example.md"
#     md_titles = ["标题1", "标题2", "标题3"]
#     md_texts = [
#         "这是第一个标题的正文。",
#         "这是第二个标题的正文。",
#         "这是第三个标题的正文。"
#     ]
#     md_image_paths = [
#         "path/to/image1.jpg",
#         "path/to/image2.jpg",
#         None  # 如果没有图片，可以设为 None
#     ]

#     # 写入Markdown内容
#     write_md_content(md_filename, md_titles, md_texts, md_image_paths)



