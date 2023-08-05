import npyscreen
import os
import shutil
import zipfile
import requests
from bs4 import BeautifulSoup


class MyForm(npyscreen.Form):
    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self):
        self.add(npyscreen.TitleText, name='设置代理端口为7890')
        os.system('set http_proxy=http://127.0.0.1:7890 & set https_proxy=http://127.0.0.1:7890')
        self.add(npyscreen.TitleText, name='搜索最新的clash')
        os.system('winget search Fndroid.ClashForWindows')

        self.add(npyscreen.TitleText, name='开始更新或者安装clash')
        self.add(npyscreen.TitleText, name='------------------------------------------------------------')
        os.system('winget install Fndroid.ClashForWindows')
        self.add(npyscreen.TitleText, name='clash更新或者安装成功')
        self.add(npyscreen.TitleText, name='------------------------------------------------------------')

        url = 'https://github.com/Fndroid/clash_for_windows_pkg'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        version = soup.select_one(
            'div.Layout-sidebar > div > div:nth-child(2) > div > a > div > div.d-flex > span').text[1:].strip()
        self.add(npyscreen.TitleText, name='获取最新版本号：' + str(version))

        self.add(npyscreen.TitleText, name='开始下载汉化包')
        self.add(npyscreen.TitleText, name='------------------------------------------------------------')
        url2 = f'https://github.com/BoyceLig/Clash_Chinese_Patch/releases/download/{version}/app.zip'
        response2 = requests.get(url2)
        with open('app.zip', 'wb') as f:
            f.write(response2.content)
        self.add(npyscreen.TitleText, name='汉化包下载成功')
        self.add(npyscreen.TitleText, name='------------------------------------------------------------')

        with zipfile.ZipFile('app.zip', 'r') as zip_ref:
            zip_ref.extractall('.')
        self.add(npyscreen.TitleText, name='文件解压完成')

        username = os.getlogin()
        self.add(npyscreen.TitleText, name='获取到用户名：' + username)

        shutil.move(
            'app.asar', f'C:\\Users\\{username}\\AppData\\Local\\Programs\\Clash for Windows\\resources\\app.asar')
        self.add(npyscreen.TitleText, name='clash汉化成功')

        os.remove('app.zip')


class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', MyForm, name='Clash 更新程序')


if __name__ == '__main__':
    myApp = MyApplication()
    myApp.run()
