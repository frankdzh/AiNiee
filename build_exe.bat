@echo off
REM ========== AiNiee 一键打包脚本 ===========

REM 1. 安装依赖（可选，已装可跳过）
REM pip install -r requirements.txt
REM pip install pyinstaller

REM 2. 清理旧的dist目录
if exist dist rmdir /s /q dist

REM 3. 打包主程序为exe
REM 出错了要结束运行，不要继续后面的步骤
python Tools\pyinstall.py
if errorlevel 1 (
    echo.
    echo ========== 打包失败！请检查错误信息 ==========
    pause
    exit /b 1
)

REM 4. 拷贝资源到dist目录
xcopy Resource dist\Resource /E /I /Y
xcopy StevExtraction dist\StevExtraction /E /I /Y
xcopy PluginScripts dist\PluginScripts /E /I /Y

REM 5. 打包完成，提示用户
echo.
echo ========== 打包完成！请到 dist 目录下找 AiNiee.exe ==========
pause 