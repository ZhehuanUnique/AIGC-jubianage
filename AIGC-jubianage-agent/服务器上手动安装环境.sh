#!/bin/bash

# 服务器上手动安装环境脚本
# 在服务器上执行：bash 服务器上手动安装环境.sh

set -e

echo "🚀 开始安装环境..."

# 更新系统
echo "📦 更新系统..."
sudo apt update && sudo apt upgrade -y

# 安装 Node.js（使用 NVM）
echo "📦 安装 Node.js..."
if [ ! -d "$HOME/.nvm" ]; then
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
fi

# 加载 NVM
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# 安装 Node.js 20
echo "📦 安装 Node.js 20..."
nvm install 20
nvm use 20
nvm alias default 20

# 验证安装
echo "✅ 验证 Node.js 安装..."
node -v
npm -v

# 安装 PM2
echo "📦 安装 PM2..."
npm install -g pm2

# 配置 PM2 开机自启
echo "📦 配置 PM2 开机自启..."
pm2 startup
echo "⚠️  请执行上面 PM2 输出的 sudo 命令"

# 安装 Nginx
echo "📦 安装 Nginx..."
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx

# 安装 Git
echo "📦 安装 Git..."
sudo apt install git -y

# 创建项目目录
echo "📦 创建项目目录..."
sudo mkdir -p /var/www/aigc-agent
sudo chown ubuntu:ubuntu /var/www/aigc-agent

# 将 NVM 添加到 .bashrc（确保每次登录都能使用）
echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.bashrc
echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.bashrc
echo '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"' >> ~/.bashrc

echo ""
echo "✅ 环境安装完成！"
echo ""
echo "📝 验证安装："
echo "   source ~/.bashrc"
echo "   node -v"
echo "   npm -v"
echo "   pm2 -v"
echo "   nginx -v"

