import winreg
import subprocess
import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

        
if is_admin():
    # input("成功以管理员身份启动")
    KEY_PATH = r'SYSTEM\CurrentControlSet\Control\Keyboard Layout'
    VALUE_NAME = 'Scancode Map'

    # 检查 Scancode Map 是否存在
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, KEY_PATH)
        value, _ = winreg.QueryValueEx(key, VALUE_NAME)
        print(f'{VALUE_NAME} 存在。')
        if value == b'\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x3a\x00\x01\x00\x01\x00\x3a\x00\x00\x00\x00\x00':
            print('当前成功映射: Esc --OK-- CapsLK')
        else:
            print('当前没有映射: Esc X----X CapsLK')
    except FileNotFoundError:
        print(f'{VALUE_NAME} 不存在。')

    # 询问用户是否要进行修改
    choice = input('您是否要修改 Scancode Map？ [y/n] ')
    if choice.lower() == 'y':
        print('1. 进行按键映射： Esc --OK-- CapsLK')
        print('2. 取消按键映射： Esc X----X CapsLK')
        option = input('输入您的选项 [1/2]: ')
        if option == '1':
            winreg.SetValueEx(key, VALUE_NAME, 0, winreg.REG_BINARY, b'\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x3a\x00\x01\x00\x01\x00\x3a\x00\x00\x00\x00\x00')
        elif option == '2':
            winreg.SetValueEx(key, VALUE_NAME, 0, winreg.REG_BINARY, b'\x00' * 20)


else:
    # 如果没有以管理员权限运行，则输出提示信息并终止代码
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
