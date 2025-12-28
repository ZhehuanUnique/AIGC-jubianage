@echo off
chcp 65001 >nul
echo ========================================
echo 项目环境检查工具
echo ========================================
echo.

echo [1/5] 检查 Node.js...
where node >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Node.js 已安装
    node --version
) else (
    echo ❌ Node.js 未安装
    echo    请访问 https://nodejs.org/ 下载安装
)
echo.

echo [2/5] 检查 npm...
where npm >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ npm 已安装
    npm --version
) else (
    echo ❌ npm 未安装
    echo    npm 通常随 Node.js 自动安装
)
echo.

echo [3/5] 检查 Python...
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python 已安装
    python --version
) else (
    echo ❌ Python 未安装
    echo    请访问 https://www.python.org/downloads/ 下载安装
    echo    ⚠️ 安装时请勾选 "Add Python to PATH"
)
echo.

echo [4/5] 检查 pip...
where pip >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ pip 已安装
    pip --version
) else (
    echo ❌ pip 未安装
    echo    pip 通常随 Python 自动安装
)
echo.

echo [5/5] 检查项目依赖...
if exist "frontend-nuxt\node_modules" (
    echo ✅ 前端依赖已安装
) else (
    echo ⚠️  前端依赖未安装
    echo    请运行: cd frontend-nuxt ^&^& npm install
)
echo.

if exist "jubianai\.env" (
    echo ✅ 后端环境变量文件已配置
) else (
    echo ⚠️  后端环境变量文件未配置
    echo    请复制 jubianai\env.example 为 jubianai\.env 并填入配置
)
echo.

echo ========================================
echo 检查完成！
echo ========================================
echo.
echo 如果所有项目都显示 ✅，说明环境已就绪
echo 如果显示 ❌ 或 ⚠️，请按照提示进行安装和配置
echo.
pause


