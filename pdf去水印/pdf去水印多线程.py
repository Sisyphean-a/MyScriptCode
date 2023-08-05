from pdf2image import convert_from_path
from PIL import Image
import cv2
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor
import shutil

def process_image(image, i):
    """
    处理单个图像。
    :param image: 要处理的图像。
    :param i: 图像的索引。
    :return: 处理后的图像和索引。
    """
    # 保存处理前的图像
    image.save(f'before/{i}.png')

    # 将 PIL 图像转换为 OpenCV 图像
    open_cv_image = np.array(image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    # 在图像上绘制矩形
    cv2.rectangle(open_cv_image, (0, 0), (1654, 80), (255, 255, 255), -1)
    cv2.rectangle(open_cv_image, (50, 2270), (600, 2300), (255, 255, 255), -1)

    # # 定义要清除的颜色范围
    # lower = np.array([190, 190, 190])
    # upper = np.array([255, 255, 255])

    # # 创建掩码
    # mask = cv2.inRange(open_cv_image, lower, upper)

    # # 应用掩码
    # open_cv_image[mask != 0] = [255, 255, 255]

    # 将 OpenCV 图像转换为 PIL 图像
    image = Image.fromarray(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))
    
    print("第" + str(i+1) + "张图片处理完毕")

    # 保存处理后的图像
    image.save(f'after/{i}.png')

    return image, i

def main():
    # 创建文件夹来保存图像
    if not os.path.exists('before'):
        os.makedirs('before')
    if not os.path.exists('after'):
        os.makedirs('after')

    # 将 PDF 文件转换为图像
    print("提取图片中，请稍后...")
    images = convert_from_path('.\\a.pdf')

    output_images = [None] * len(images)

    with ThreadPoolExecutor() as executor:
        results = [executor.submit(process_image, image, i) for i, image in enumerate(images)]
        
        for f in results:
            image, i = f.result()
            output_images[i] = image

    # 保存 PDF 文件
    output_images[0].save('output.pdf', save_all=True, append_images=output_images[1:])

    # 删除 before 和 after 文件夹
    shutil.rmtree('before')
    shutil.rmtree('after')

if __name__ == '__main__':
     main()
