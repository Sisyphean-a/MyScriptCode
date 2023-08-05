import subprocess
import ctypes
import sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    # {code}
    input("成功以管理员身份启动")
else:
    # 如果没有以管理员权限运行，则输出提示信息并终止代码
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
