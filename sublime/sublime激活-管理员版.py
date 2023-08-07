import ctypes
import sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    # 在这里添加原来的代码
    old_hex_string = '807805000f94c1'
    new_hex_string = 'c64005014885c9'
    # old_hex_string = 'c64005014885c9'
    # new_hex_string = '807805000f94c1'

    with open('C:\\Program Files\\Sublime Text\\sublime_text.exe', 'rb') as f:
        binary_data = f.read()
        hex_data = binary_data.hex()
        # 搜索旧的十六进制字符串
        if old_hex_string in hex_data:
            print('查找成功')
            # 替换旧的十六进制字符串为新的十六进制字符串
            new_hex_data = hex_data.replace(old_hex_string, new_hex_string)
            # 将十六进制数据转换回二进制数据
            new_binary_data = bytes.fromhex(new_hex_data)
            # 将修改后的二进制数据写回文件
            with open('C:\\Program Files\\Sublime Text\\sublime_text.exe', 'wb') as f:
                f.write(new_binary_data)
            print('修改成功')
        else:
            print('未找到元素')

    input("Please enter any key to continue")
else:
    # 如果没有以管理员权限运行，则输出提示信息并终止代码
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
