from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import os


def add_grid(image, spacing=100):
    """
    在图像上添加带有标尺和网格的图层。
    :param image: 要添加网格的图像。
    :param spacing: 网格线之间的间距（以像素为单位）。
    :return: 添加了网格的图像。
    """
    # 创建一个新的透明图层
    grid_layer = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(grid_layer)

    # 获取图像的宽度和高度
    width, height = image.size

    # 绘制水平线
    for y in range(0, height, spacing):
        draw.line((0, y, width, y), fill=(0, 0, 0, 128))

        # 添加数字标识
        font = ImageFont.truetype("arial.ttf", 16)
        draw.text((0, y), str(y), fill=(0, 0, 0), font=font)

    # 绘制垂直线
    for x in range(0, width, spacing):
        draw.line((x, 0, x, height), fill=(0, 0, 0, 128))

        # 添加数字标识
        font = ImageFont.truetype("arial.ttf", 16)
        draw.text((x, 0), str(x), fill=(0, 0, 0), font=font)

    # 将网格层与原始图像合并
    return Image.alpha_composite(image.convert('RGBA'), grid_layer).convert('RGB')


def pil_to_cv(image):
    """
    将 PIL 图像转换为 OpenCV 图像。
    :param image: 要转换的 PIL 图像。
    :return: 转换后的 OpenCV 图像。
    """
    open_cv_image = np.array(image)
    return open_cv_image[:, :, ::-1].copy()


def cv_to_pil(image):
    """
    将 OpenCV 图像转换为 PIL 图像。
    :param image: 要转换的 OpenCV 图像。
    :return: 转换后的 PIL 图像。
    """
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


def main(image):
    # 将 PIL 图像转换为 OpenCV 图像
    open_cv_image = pil_to_cv(image)

    # 获取图像的宽度和高度
    height, width, _ = open_cv_image.shape
    print(f'测得高度为：{height}\n测得宽度为：{width}\n')

    # 在图像上绘制矩形
    # cv2.rectangle(image, 左上角左边xy, 右下角坐标xy, color, thickness)
    # color可以测试环境使用(0,0,255),生产环境使用(255,255,255)
    cv2.rectangle(open_cv_image, (0, 0), (1654, 80), (0, 0, 255), -1)
    cv2.rectangle(open_cv_image, (0, 1700), (110, 1900), (0, 0, 255), -1)
    cv2.rectangle(open_cv_image, (0, 1820), (1500, 1900), (0, 0, 255), -1)
    # cv2.rectangle(open_cv_image, (50, 2270), (600, 2300), (0, 0, 255), -1)

    # 将 OpenCV 图像转换为 PIL 图像
    image = cv_to_pil(open_cv_image)

    # 保存处理后的图像
    # image = add_grid(image)
    image.save('测试后.png')


if __name__ == '__main__':
    # 检查当前目录中是否存在名为“测试前.png”的文件
    if os.path.exists('测试前.png'):
        image = Image.open('测试前.png')
    else:
        print("提取测试图片中，请稍后...")
        images = convert_from_path('.\\a.pdf')
        image = images[5]
        # 在图像上添加网格
        image = add_grid(image)
        # 保存处理前的图像
        image.save('测试前.png')

    main(image)
