import os
import re
from aip import AipOcr
from PIL import Image

APP_ID = '26391797'
API_KEY = 'tdrnqEyU3ULlF74QHwBWT997'
SECRET_KEY = 'bEndqOa0e4iNpKVq57b0ZdqqbiqmBfdm'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def ocr_image(image_path):
    image = get_file_content(image_path)
    result = client.basicGeneral(image)
    if 'words_result' in result:
        return '\n'.join([w['words'] for w in result['words_result']])
    else:
        return ''

def crop_image(image_path):
    with Image.open(image_path) as im:
        width, height = im.size
        cropped_image = im.crop((0, height - 125, width, height))
        cropped_image.save('cropped.jpg')

for file in os.listdir('.'):
    if file.endswith('.jpg') or file.endswith('.JPG'):
        if file == 'cropped.jpg':
            continue
        crop_image(file)
        text = ocr_image('cropped.jpg')
        # print(f'Text to match: {text}')
        if '\n' in text:
            # 如果文本中包含换行符，那么直接将第一行作为姓名，第二行作为身份证号码
            lines = text.split('\n')
            name = lines[0]
            id_number = lines[1]
        else:
            # 如果文本中不包含换行符，那么使用正则表达式来匹配姓名和身份证号码
            match = re.search(r'([\u4e00-\u9fa5]+)(\d+[Xx]?)', text)
            # print(match)
            if match:
                name, id_number = match.groups()
            else:
                name, id_number = None, None
        if name and id_number:
            new_name = f'{name}+男+身份证+{id_number}.jpg'
            # print(f'New file name: {new_name}')
            if os.path.exists(new_name):
                print(f'文件 {new_name} 已经存在，跳过重命名操作')
            else:
                os.rename(file, new_name)
            print(f'{name}---完成处理')
os.remove('cropped.jpg')
