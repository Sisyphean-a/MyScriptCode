import os
import shutil
import zipfile
import requests
from bs4 import BeautifulSoup

print("                  设置代理端口为7890")
os.system('set http_proxy=http://127.0.0.1:7890 & set https_proxy=http://127.0.0.1:7890')
print("                   搜索最新的clash")
os.system('winget search Fndroid.ClashForWindows')
print("\n\n")

print("                 开始更新或者安装clash")
print("------------------------------------------------------------")
# 安装 Fndroid.ClashForWindows
os.system('winget install Fndroid.ClashForWindows')
print("                  clash更新或者安装成功")
print("------------------------------------------------------------")
print("\n\n")

# 获取最新版本号
url = 'https://github.com/Fndroid/clash_for_windows_pkg'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
version = soup.select_one('div.Layout-sidebar > div > div:nth-child(2) > div > a > div > div.d-flex > span').text[1:].strip()
print("                    获取最新版本号：" + str(version))
print("\n\n")

# 下载第二个资源
print("                    开始下载汉化包")
print("------------------------------------------------------------")
url2 = f'https://github.com/BoyceLig/Clash_Chinese_Patch/releases/download/{version}/app.zip'
response2 = requests.get(url2)
with open('app.zip', 'wb') as f:
    f.write(response2.content)
print("                   汉化包下载成功")
print("------------------------------------------------------------")
print("\n\n")

# 解压 app.zip 文件
with zipfile.ZipFile('app.zip', 'r') as zip_ref:
    zip_ref.extractall('.')
print("                   文件解压完成")

# 获取当前用户的用户名
username = os.getlogin()
print("                   获取到用户名：" + username)

# 移动 app.asar 文件到指定目录并替换原有文件
shutil.move('app.asar', f'C:\\Users\\{username}\\AppData\\Local\\Programs\\Clash for Windows\\resources\\app.asar')
print("                   clash汉化成功")
print("\n\n")

# 删除 app.zip 文件
os.remove('app.zip')

input('Press Enter to exit...')

