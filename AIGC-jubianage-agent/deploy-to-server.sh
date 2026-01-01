#!/bin/bash

# 腾讯云服务器自动部署脚本
# 使用方法：在服务器上执行此脚本

set -e  # 遇到错误立即退出

echo "🚀 开始自动部署 AIGC Agent 到腾讯云服务器..."

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 服务器信息
SERVER_IP="119.45.121.152"
DOMAIN="jubianai.cn"
PROJECT_DIR="/var/www/aigc-agent"

# 第一步：更新系统
echo -e "${YELLOW}📦 步骤 1/6: 更新系统...${NC}"
sudo apt update && sudo apt upgrade -y

# 第二步：安装 Node.js
echo -e "${YELLOW}📦 步骤 2/6: 安装 Node.js...${NC}"
if ! command -v node &> /dev/null; then
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    nvm install 20
    nvm use 20
    nvm alias default 20
    echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.bashrc
    echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.bashrc
    echo '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"' >> ~/.bashrc
    source ~/.bashrc
else
    echo -e "${GREEN}✅ Node.js 已安装${NC}"
fi

# 验证 Node.js
echo -e "${GREEN}Node.js 版本:${NC}"
node -v
echo -e "${GREEN}npm 版本:${NC}"
npm -v

# 第三步：安装 PM2
echo -e "${YELLOW}📦 步骤 3/6: 安装 PM2...${NC}"
if ! command -v pm2 &> /dev/null; then
    npm install -g pm2
    pm2 startup
    echo -e "${YELLOW}⚠️  请执行上面 PM2 输出的 sudo 命令来设置开机自启${NC}"
else
    echo -e "${GREEN}✅ PM2 已安装${NC}"
fi

# 第四步：安装 Nginx
echo -e "${YELLOW}📦 步骤 4/6: 安装 Nginx...${NC}"
if ! command -v nginx &> /dev/null; then
    sudo apt install nginx -y
    sudo systemctl start nginx
    sudo systemctl enable nginx
else
    echo -e "${GREEN}✅ Nginx 已安装${NC}"
fi

# 第五步：安装 Git
echo -e "${YELLOW}📦 步骤 5/6: 安装 Git...${NC}"
if ! command -v git &> /dev/null; then
    sudo apt install git -y
else
    echo -e "${GREEN}✅ Git 已安装${NC}"
fi

# 第六步：创建项目目录
echo -e "${YELLOW}📦 步骤 6/6: 创建项目目录...${NC}"
sudo mkdir -p $PROJECT_DIR
sudo chown ubuntu:ubuntu $PROJECT_DIR

echo -e "${GREEN}✅ 环境安装完成！${NC}"
echo -e "${YELLOW}📝 下一步：请从 Windows 上传代码到服务器${NC}"
echo -e "${YELLOW}   在 Windows PowerShell 中执行: .\upload-to-server.ps1${NC}"
