@echo off
chcp 65001 >nul
echo ========================================
echo 检查视频上传环境
echo ========================================
echo.

REM 检查 Python
echo [1] 检查 Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 未安装或不在 PATH 中
    echo 请安装 Python 3.11 或更高版本
) else (
    python --version
    echo ✅ Python 已安装
)
echo.

REM 检查 COS SDK
echo [2] 检查 cos-python-sdk-v5...
python -c "import qcloud_cos; print('✅ cos-python-sdk-v5 已安装')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ cos-python-sdk-v5 未安装
    echo 请运行: pip install cos-python-sdk-v5
) else (
    echo ✅ cos-python-sdk-v5 已安装
)
echo.

REM 检查视频文件
echo [3] 检查视频文件...
if exist "index.mp4" (
    echo ✅ 找到 index.mp4
) else (
    echo ⚠️  未找到 index.mp4
)

if exist "index.webm" (
    echo ✅ 找到 index.webm
) else (
    echo ⚠️  未找到 index.webm
)

if exist "frontend-nuxt\public\index.mp4" (
    echo ✅ 找到 frontend-nuxt\public\index.mp4
) else (
    echo ⚠️  未找到 frontend-nuxt\public\index.mp4
)

if exist "frontend-nuxt\public\index.webm" (
    echo ✅ 找到 frontend-nuxt\public\index.webm
) else (
    echo ⚠️  未找到 frontend-nuxt\public\index.webm
)
echo.

echo ========================================
echo 检查完成
echo ========================================
pause

