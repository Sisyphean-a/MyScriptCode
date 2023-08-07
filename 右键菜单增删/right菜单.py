import winreg
from tkinter import Tk, Label, Button, Checkbutton, IntVar
import subprocess
import ctypes
import sys
from tkinter import messagebox

# pyinstaller -F -w right菜单.py

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def add_file_type(file_type, file_path):
    if file_type == ".md":
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, file_type, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "Typora.md")
        winreg.CloseKey(key)
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, file_type + "\\ShellNew")
        winreg.SetValueEx(key, "NullFile", 0, winreg.REG_SZ, "")
        winreg.CloseKey(key)
    else:
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, file_type + "\\ShellNew")
        winreg.SetValueEx(key, "FileName", 0, winreg.REG_SZ, file_path)
        winreg.CloseKey(key)


def remove_file_type(file_type):
    try:
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, file_type + "\\ShellNew")
    except WindowsError:
        pass


def apply_changes(add_vars, remove_vars):
    try:
        for file_type, var in add_vars.items():
            if var.get() == 1:
                add_file_type(file_type, "C:\\Windows\\ShellNew\\" + file_type[1:] + ".txt")
        for file_type, var in remove_vars.items():
            if var.get() == 1:
                remove_file_type(file_type)
        messagebox.showinfo("Success", "操作成功！")
    except Exception as e:
        messagebox.showerror("Error", f"操作失败: {e}")


def main():
    root = Tk()
    root.geometry("400x200")
    root.title("Add/Remove File Types")

    Label(root, text="Add File Types:").grid(row=0, column=0, sticky="ew")
    Label(root, text="Remove File Types:").grid(row=0, column=1, sticky="ew")

    add_file_types = [".md", ".py", ".ps1", ".bat"]
    remove_file_types = [".bmp", ".lnk", ".zip", ".paint", ".rft"]
    add_vars = {}
    remove_vars = {}

    for i, file_type in enumerate(add_file_types):
        add_vars[file_type] = IntVar()
        Checkbutton(root, text=file_type, variable=add_vars[file_type]).grid(row=i + 1, column=0, sticky="w", padx=20)
    for i, file_type in enumerate(remove_file_types):
        remove_vars[file_type] = IntVar()
        Checkbutton(root, text=file_type, variable=remove_vars[file_type]).grid(
            row=i + 1, column=1, sticky="w", padx=20)

    Button(root, text="Add", command=lambda: apply_changes(add_vars, {})).grid(
        row=max(len(add_file_types), len(remove_file_types)) + 2, column=0, sticky="ew")
    Button(root, text="Remove", command=lambda: apply_changes({}, remove_vars)).grid(
        row=max(len(add_file_types), len(remove_file_types)) + 2, column=1, sticky="ew")

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    for i in range(max(len(add_file_types), len(remove_file_types)) + 2):
        root.rowconfigure(i, weight=1)

    root.mainloop()


if __name__ == "__main__":
    if is_admin():
        main()
    else:
        # 如果没有以管理员权限运行，则输出提示信息并终止代码
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
