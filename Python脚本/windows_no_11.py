import winreg
import subprocess
import ctypes
import sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def check():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate", 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, "TargetReleaseVersionInfo")
        print(f"当前限制策略为: {value}\n")
    except FileNotFoundError:
        print("当前限制策略为: 未限制更改\n")
    except Exception as e:
        print(f"Error: {e}")


def restore():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SOFTWARE\Policies\Microsoft\Windows", 0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteKey(key, "WindowsUpdate")
        print("WindowsUpdate key deleted.")
    except FileNotFoundError:
        print("WindowsUpdate key not found.")
    except Exception as e:
        print(f"Error: {e}")


def modify():
    try:
        key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE,
                                 r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate", 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, "TargetReleaseVersion", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(key, "TargetReleaseVersionInfo", 0, winreg.REG_SZ, "22H2")
        print("WindowsUpdate key modified.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if is_admin():
        check()
        print("选项：\n1. 修改注册表阻止系统更新成Windows11\n2. 恢复对注册表的修改\n")
        action = input("请选择: ")
        if action == "2":
            restore()
            input("恢复完成....")
        elif action == "1":
            modify()
            input("修改完成....")
        else:
            input("你没有进行任何操作")
    else:
        # 如果没有以管理员权限运行，则输出提示信息并终止代码
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
