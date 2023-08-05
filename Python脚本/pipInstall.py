import subprocess
import sys

packages = ['windows-curses',
            'npyscreen',
            'requests',
            'bs4',
            'pipenv',
            'opencv-python',
            'pyinstaller']


def check_installed_packages():
    installed = []
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    return installed_packages


def install_packages(packages):
    for package in packages:
        try:
            subprocess.check_call(["pip", "install", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", package])
            print(f"{package} 安装成功")
        except subprocess.CalledProcessError:
            print(f"{package} 安装失败")


if __name__ == '__main__':
    print("目标包：")
    for package in packages:
        print(f"       {package}")

    print("\n正在检查已安装的包，请稍候...")
    installed_packages = check_installed_packages()

    not_installed_packages = []
    for package in packages:
        if package in installed_packages:
            print(f"     ✓ {package}")
        else:
            print(f"     ✗ {package}")
            not_installed_packages.append(package)

    if not_installed_packages:
        answer = input("\n是否需要安装未安装的包？(y/n)")
        if answer.lower() == 'y':
            install_packages(not_installed_packages)
