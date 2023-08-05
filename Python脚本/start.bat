@echo off
chcp 65001
setlocal enabledelayedexpansion
set i=0
for %%f in (*.py) do (
    set /a i+=1
    set "options[!i!]=%%f"
    echo !i!. %%f
)
set /p choice=请选择一个文件运行: 
start cmd /k "python .\!options[%choice%]! && echo 运行成功 || echo 运行失败"
