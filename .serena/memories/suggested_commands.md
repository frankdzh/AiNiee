# AiNiee 建议命令列表

## 开发环境设置
```powershell
# 安装依赖
pip install -r requirements.txt

# 安装打包工具
pip install pyinstaller
```

## 运行项目
```powershell
# 启动主程序
python AiNiee.py
```

## 打包和构建
```powershell
# 一键打包为可执行文件
build_exe.bat

# 手动打包（如果批处理文件有问题）
python Tools\pyinstall.py
```

## 开发工具命令
```powershell
# 查看项目结构
dir /s

# 搜索文件
findstr /s /i "关键词" *.py

# 查看文件内容
type filename.py

# 复制文件
copy source.py destination.py

# 移动文件
move source.py destination.py

# 删除文件
del filename.py

# 创建目录
mkdir dirname

# 删除目录
rmdir /s dirname
```

## Git 命令（如果使用版本控制）
```powershell
# 查看状态
git status

# 添加文件
git add .

# 提交更改
git commit -m "commit message"

# 推送到远程
git push

# 拉取更新
git pull

# 查看日志
git log --oneline
```

## 调试和测试
```powershell
# 运行特定模块测试
python -m ModuleFolders.RequestTester.RequestTester

# 检查语法错误
python -m py_compile filename.py
```

## 清理命令
```powershell
# 清理 Python 缓存
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"

# 清理构建文件
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
```