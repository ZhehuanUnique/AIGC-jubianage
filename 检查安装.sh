#!/bin/bash

echo "========================================"
echo "项目环境检查工具"
echo "========================================"
echo ""

echo "[1/5] 检查 Node.js..."
if command -v node &> /dev/null; then
    echo "✅ Node.js 已安装"
    node --version
else
    echo "❌ Node.js 未安装"
    echo "   请访问 https://nodejs.org/ 下载安装"
fi
echo ""

echo "[2/5] 检查 npm..."
if command -v npm &> /dev/null; then
    echo "✅ npm 已安装"
    npm --version
else
    echo "❌ npm 未安装"
    echo "   npm 通常随 Node.js 自动安装"
fi
echo ""

echo "[3/5] 检查 Python..."
if command -v python3 &> /dev/null; then
    echo "✅ Python 已安装"
    python3 --version
elif command -v python &> /dev/null; then
    echo "✅ Python 已安装"
    python --version
else
    echo "❌ Python 未安装"
    echo "   请访问 https://www.python.org/downloads/ 下载安装"
fi
echo ""

echo "[4/5] 检查 pip..."
if command -v pip3 &> /dev/null; then
    echo "✅ pip 已安装"
    pip3 --version
elif command -v pip &> /dev/null; then
    echo "✅ pip 已安装"
    pip --version
else
    echo "❌ pip 未安装"
    echo "   pip 通常随 Python 自动安装"
fi
echo ""

echo "[5/5] 检查项目依赖..."
if [ -d "frontend-nuxt/node_modules" ]; then
    echo "✅ 前端依赖已安装"
else
    echo "⚠️  前端依赖未安装"
    echo "   请运行: cd frontend-nuxt && npm install"
fi
echo ""

if [ -f "jubianai/.env" ]; then
    echo "✅ 后端环境变量文件已配置"
else
    echo "⚠️  后端环境变量文件未配置"
    echo "   请复制 jubianai/env.example 为 jubianai/.env 并填入配置"
fi
echo ""

echo "========================================"
echo "检查完成！"
echo "========================================"
echo ""
echo "如果所有项目都显示 ✅，说明环境已就绪"
echo "如果显示 ❌ 或 ⚠️，请按照提示进行安装和配置"
echo ""


