import winreg


def check_file_type(file_type):
    try:
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, file_type + "\\ShellNew")
        winreg.CloseKey(key)
        print(f"{file_type} 文件类型已成功添加。")
    except WindowsError:
        print(f"{file_type} 文件类型未添加或已删除。")


def main():
    add_file_types = [".md", ".py", ".ps1"]
    remove_file_types = [".bmp", ".lnk", ".zip", ".paint", ".rft"]
    for file_type in add_file_types + remove_file_types:
        check_file_type(file_type)


if __name__ == "__main__":
    main()
    input("按回车键继续....")
