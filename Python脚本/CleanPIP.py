import os
from datetime import datetime
from importlib.metadata import distributions
from datetime import timedelta


def get_installed_packages():
    print("----------------error------------------")
    packages = []
    for package in distributions():
        try:
            location = package.locate_file('')
            timestamp = os.path.getctime(str(location))
            dt_object = datetime.fromtimestamp(timestamp)
            formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
            packages.append((dt_object, "{} | {}".format(formatted_time, package.metadata['Name'])))
        except OSError:
            print("无法获取 {} 包的安装时间".format(package.metadata['Name']))

    packages.sort(key=lambda x: x[0])
    print("---------time-------|-------start-----------")
    return packages

packages = get_installed_packages()
for _, package_info in packages:
    print(package_info)
print("---------time-------|-------stop-----------\n\n")

def uninstall_packages(time_frame):
    now = datetime.now()
    all_packages = get_installed_packages()
    packages_to_uninstall = [package_info[1] for package_info in all_packages if now - package_info[0] <= time_frame]

    if packages_to_uninstall:
        print("将卸载以下包：")
        for package in packages_to_uninstall:
            print(package)
        os.system('pip uninstall -y ' + ' '.join(packages_to_uninstall))
    else:
        print("没有找到符合条件的包")

print("请选择一个选项：\n" +
        "a. 卸载一个小时内安装的包\n" +
        "b. 卸载三个小时内安装的包\n" +
        "c. 卸载今天安装的包\n" +
        "d. 不卸载任何包")

choice = input("请输入你的选择：")

if choice == 'a':
    uninstall_packages(timedelta(hours=1))
elif choice == 'b':
    uninstall_packages(timedelta(hours=3))
elif choice == 'c':
    uninstall_packages(timedelta(days=1))
elif choice == 'd':
    print("未选择卸载任何包")
else:
    print("无效的选择")
