import os
import shutil
import subprocess
from shutil import which


def check_pyinstaller():
    if which('pyinstaller') is None:
        if which('pip') is not None:
            subprocess.run(['pip', 'install', 'pyinstaller'])
        elif which('python') is not None:
            print('请先安装 pip')
            return False
        else:
            print('请先安装 python')
            return False
    return True


def get_py_files():
    # 获取当前目录下所有 .py 文件并排序
    py_files = sorted([f for f in os.listdir() if f.endswith('.py')])
    return py_files


def print_py_files(py_files):
    # 输出文件列表
    print('当前目录下的 .py 文件：')
    for i, file in enumerate(py_files):
        print(f'{i + 1}. {file}')


def get_target_file(py_files):
    # 询问用户要打包哪个文件
    file_num = int(input('请输入要打包的文件序号：'))
    target_file = py_files[file_num - 1]
    return target_file


def package_file(target_file):
    # 使用 pyinstaller 进行打包
    subprocess.run(['pyinstaller', '--onefile', target_file])


def move_file(target_file):
    # 如果当前已经存在打包过的单文件，则先删除旧文件在移动新文件
    if os.path.exists(f'{target_file[:-3]}.exe'):
        os.remove(f'{target_file[:-3]}.exe')
    os.rename(f'dist/{target_file[:-3]}.exe', f'{target_file[:-3]}.exe')

    # 做一个检测，如果存在__pycache__目录才删除__pycache__目录
    if os.path.exists('__pycache__'):
        shutil.rmtree('__pycache__')
    shutil.rmtree('build')
    shutil.rmtree('dist')
    os.remove(f'{target_file[:-3]}.spec')


if __name__ == '__main__':
    if check_pyinstaller():
        py_files = get_py_files()
        print_py_files(py_files)
        target_file = get_target_file(py_files)
        package_file(target_file)
        move_file(target_file)
        input("打包完成，回车键关闭程序...")
