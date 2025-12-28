@echo off
chcp 65001 >nul
echo ========================================
echo 测试 COS 连接
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

REM 运行测试脚本
python 测试COS连接.py

pause

