@echo off
echo ========================================
echo 安装 doubao-rag 依赖（禁用代理）
echo ========================================
echo.

REM 禁用所有代理
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=
set NO_PROXY=*
set no_proxy=*

echo 已禁用代理设置
echo.

echo [1/5] 安装基础依赖（使用清华镜像）...
pip install fastapi uvicorn python-multipart pydantic opencv-python pillow numpy -i https://pypi.tuna.tsinghua.edu.cn/simple
if errorlevel 1 (
    echo 基础依赖安装失败！
    pause
    exit /b 1
)

echo.
echo [2/5] 安装 LangGraph（使用清华镜像）...
pip install langgraph langchain langchain-core -i https://pypi.tuna.tsinghua.edu.cn/simple
if errorlevel 1 (
    echo LangGraph 安装失败！
    pause
    exit /b 1
)

echo.
echo [3/5] 安装预编译的 tokenizers（避免 Rust 编译，使用清华镜像）...
pip install tokenizers --only-binary :all: -i https://pypi.tuna.tsinghua.edu.cn/simple
if errorlevel 1 (
    echo tokenizers 安装失败！
    pause
    exit /b 1
)

echo.
echo [4/5] 安装 sentence-transformers（使用清华镜像）...
pip install sentence-transformers -i https://pypi.tuna.tsinghua.edu.cn/simple
if errorlevel 1 (
    echo sentence-transformers 安装失败！
    pause
    exit /b 1
)

echo.
echo [5/5] 安装 chromadb（使用清华镜像）...
pip install chromadb -i https://pypi.tuna.tsinghua.edu.cn/simple
if errorlevel 1 (
    echo chromadb 安装失败！
    pause
    exit /b 1
)

echo.
echo [可选] 安装 ffmpeg-python...
pip install ffmpeg-python -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo ========================================
echo 安装完成！
echo ========================================
pause


