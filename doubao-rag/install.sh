#!/bin/bash

echo "========================================"
echo "安装 doubao-rag 依赖"
echo "========================================"
echo

echo "[1/5] 安装基础依赖..."
pip install fastapi uvicorn python-multipart pydantic opencv-python pillow numpy || exit 1

echo
echo "[2/5] 安装 LangGraph..."
pip install langgraph langchain langchain-core || exit 1

echo
echo "[3/5] 安装预编译的 tokenizers（避免 Rust 编译）..."
pip install tokenizers --only-binary :all: || {
    echo "tokenizers 安装失败！尝试使用国内镜像..."
    pip install tokenizers --only-binary :all: -i https://pypi.tuna.tsinghua.edu.cn/simple || exit 1
}

echo
echo "[4/5] 安装 sentence-transformers..."
pip install sentence-transformers || exit 1

echo
echo "[5/5] 安装 chromadb..."
pip install chromadb || exit 1

echo
echo "[可选] 安装 ffmpeg-python..."
pip install ffmpeg-python

echo
echo "========================================"
echo "安装完成！"
echo "========================================"




