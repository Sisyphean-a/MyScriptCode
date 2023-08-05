## pipenv

```shell
# 安装,建议使用管理员模式打开powershell
pip3 install pipenv

# 创建虚拟环境
mkdir projeck
cd projeck 
pipenv install

# 生成了两个文件：
# Pipfile : 配置文件，可以使用pipenv install --dev复刻
# Pipfile.lock : 哈希值

# 安装包与卸载包
pip list
pipenv install opencv-python
pipenv uninstall opencv-python

# 启动虚拟环境
pipenv shell

# 删除虚拟环境
pipenv --rm
# 或者根据路径直接删除对应的文件夹
pipenv --venv                  



```

