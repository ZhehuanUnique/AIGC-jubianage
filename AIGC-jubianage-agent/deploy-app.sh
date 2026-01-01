#!/bin/bash

# 应用部署脚本
# 在服务器上执行（代码已上传后）

set -e

PROJECT_DIR="/var/www/aigc-agent"
DOMAIN="jubianai.cn"

echo "🚀 开始部署应用..."

cd $PROJECT_DIR

# 检查 .env 文件
if [ ! -f "server/.env" ]; then
    echo "❌ 错误: server/.env 文件不存在"
    echo "请先配置环境变量: cd server && cp env.example .env && nano .env"
    exit 1
fi

# 安装前端依赖
echo "📦 安装前端依赖..."
npm install

# 创建生产环境变量文件
echo "📝 创建生产环境变量..."
cat > .env.production <<EOF
VITE_API_BASE_URL=https://${DOMAIN}/api
EOF

# 构建前端
echo "🔨 构建前端..."
npm run build

# 安装后端依赖
echo "📦 安装后端依赖..."
cd server
npm install

# 测试环境变量
echo "🔍 测试环境变量..."
npm run check-env || echo "⚠️  环境变量检查失败，请检查 .env 文件"

# 启动后端服务
echo "🚀 启动后端服务..."
pm2 restart aigc-backend || pm2 start index.js --name aigc-backend
pm2 save

# 查看状态
pm2 status
pm2 logs aigc-backend --lines 20

echo "✅ 应用部署完成！"
echo "🌐 访问: https://${DOMAIN}"

