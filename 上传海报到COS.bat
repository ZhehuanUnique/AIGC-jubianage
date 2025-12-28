@echo off
chcp 65001 >nul
echo ========================================
echo 上传海报到腾讯云 COS
echo ========================================
echo.

REM 检查 Python 是否安装
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到 Python，请先安装 Python
    pause
    exit /b 1
)

REM 检查上传脚本是否存在
if not exist "upload_posters_to_cos.py" (
    echo ❌ 错误: 未找到 upload_posters_to_cos.py
    pause
    exit /b 1
)

REM 检查桌面上的 poster 文件夹
if not exist "C:\Users\Administrator\Desktop\poster" (
    echo ❌ 错误: 未找到桌面上的 poster 文件夹
    echo 路径: C:\Users\Administrator\Desktop\poster
    pause
    exit /b 1
)

echo ✅ 检查通过，开始上传...
echo.

REM 运行上传脚本
python upload_posters_to_cos.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ 上传失败，错误代码: %errorlevel%
    pause
    exit /b 1
)

echo.
echo ✅ 上传完成！
pause

