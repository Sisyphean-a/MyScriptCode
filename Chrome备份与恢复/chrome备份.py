import ctypes
import os
import shutil
import sys
import zipfile
from pathlib import Path
import subprocess

def close_chrome():
    subprocess.call("taskkill /F /IM chrome.exe", shell=True)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def backup():
    close_chrome()
    src = Path("C:/Users/xiakn/AppData/Local/Google/Chrome/User Data/Default")
    dst = Path(os.getcwd()) / "Default.zip"
    try:
        with zipfile.ZipFile(dst, "w") as zf:
            for root, dirs, files in os.walk(src):
                if Path(root).parent == src:
                    print(f"Backing up: {Path(root).name}")
                for file in files:
                    # print(f"Backing up: {file}")
                    try:
                        zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), src))
                    except Exception as e:
                        print(f"Error: {e}")
                        input(" ")
    except Exception as e:
        print(f"Error: {e}")
        input(" ")
        os.remove(dst)


def restore():
    close_chrome()
    src = Path(os.getcwd()) / "Default.zip"
    dst = Path("C:/Users/xiakn/AppData/Local/Google/Chrome/User Data")
    try:
        print("正在移动压缩包文件...")
        shutil.copy(src, dst)
        print("压缩包文件移动完成")
        if (dst / "Default").exists():
            print("检测到对应的Default目录，开始删除...")
            shutil.rmtree(dst / "Default")
            print("已删除原有的Default目录")
        with zipfile.ZipFile(dst / "Default.zip", "r") as zf:
            print("开始解压...")
            zf.extractall(dst / "Default")
        print("解压完成，清理对应目录的Default.zip文件")
        os.remove(dst / "Default.zip")
    except Exception as e:
        print(f"Error: {e}")



if is_admin():
    choice = input("请选择对谷歌浏览器当前用户信息的操作：\n1. 备份\n2. 恢复\n")
    if choice == "1":
        backup()
        print("备份完成")
    elif choice == "2":
        restore()
        print("恢复完成")
    input("Please press any key to continue!")
else:
    # 请求管理员权限并重新启动脚本
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
