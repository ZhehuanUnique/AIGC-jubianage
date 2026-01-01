#!/bin/bash

# 腾讯云部署脚本
# 使用方法: ./deploy.sh

set -e  # 遇到错误立即退出

echo "🚀 开始部署 AIGC Agent 到腾讯云..."

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查是否在项目根目录
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ 错误: 请在项目根目录执行此脚本${NC}"
    exit 1
fi

# 1. 拉取最新代码
echo -e "${YELLOW}📥 拉取最新代码...${NC}"
git pull origin main || git pull origin master

# 2. 安装前端依赖
echo -e "${YELLOW}📦 安装前端依赖...${NC}"
npm install

# 3. 检查环境变量
if [ ! -f "server/.env" ]; then
    echo -e "${RED}❌ 错误: server/.env 文件不存在，请先配置环境变量${NC}"
    exit 1
fi

# 4. 构建前端
echo -e "${YELLOW}🔨 构建前端...${NC}"
npm run build

# 5. 安装后端依赖
echo -e "${YELLOW}📦 安装后端依赖...${NC}"
cd server
npm install
cd ..

# 6. 重启后端服务
echo -e "${YELLOW}🔄 重启后端服务...${NC}"
pm2 restart aigc-backend || pm2 start server/index.js --name aigc-backend

# 7. 重新加载 Nginx
echo -e "${YELLOW}🔄 重新加载 Nginx...${NC}"
sudo nginx -t && sudo systemctl reload nginx

echo -e "${GREEN}✅ 部署完成！${NC}"
echo -e "${GREEN}📊 查看服务状态: pm2 status${NC}"
echo -e "${GREEN}📋 查看日志: pm2 logs aigc-backend${NC}"

