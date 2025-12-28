@echo off
chcp 65001 >nul
echo ========================================
echo 上传海报到腾讯云 COS
echo ========================================
echo.

cd /d "%~dp0"

REM 检查 Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到 Python
    pause
    exit /b 1
)

REM 检查脚本
if not exist "upload_posters_to_cos_direct.py" (
    echo ❌ 错误: 未找到上传脚本
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

python upload_posters_to_cos_direct.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ 上传失败
    pause
    exit /b 1
)

echo.
pause

