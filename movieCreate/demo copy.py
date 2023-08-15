from PIL import Image

# 读取原始灰度图像
gray_image = Image.open('/Users/sqb/Documents/shengcai/movieCreate/imgs_folder/20190204281620_eamNTG.gif').convert('L')
# gray_image = Image.open('/Users/sqb/Documents/shengcai/movieCreate/imgs_folder/20170514722329_XBROqZ.gif').convert('L')

# 获取图像的宽度和高度
width, height = gray_image.size

# 创建新的RGB图像
rgb_image = Image.new('RGB', (width, height))

# 对每个像素进行颜色映射
for y in range(height):
    for x in range(width):
        gray_value = gray_image.getpixel((x, y))
        rgb_value = (gray_value, gray_value, gray_value)
        rgb_image.putpixel((x, y), rgb_value)

# 保存新的RGB图像
rgb_image.save('/Users/sqb/Documents/shengcai/movieCreate/output/111.png')

print("转换完成！")
