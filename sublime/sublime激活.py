old_hex_string = '807805000f94c1'
# old_hex_string = 'c64005014885c9'
new_hex_string = 'c64005014885c9'

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