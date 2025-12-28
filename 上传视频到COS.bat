@echo off
chcp 65001 >nul
echo ========================================
echo 上传视频文件到腾讯云 COS
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
if not exist "upload_videos_to_cos.py" (
    echo ❌ 错误: 未找到上传脚本
    pause
    exit /b 1
)

echo ✅ 检查通过，开始上传...
echo.

python upload_videos_to_cos.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ 上传失败
    pause
    exit /b 1
)

echo.
pause

