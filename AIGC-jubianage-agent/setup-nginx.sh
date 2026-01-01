#!/bin/bash

# Nginx 配置脚本
# 在服务器上执行

DOMAIN="jubianai.cn"
PROJECT_DIR="/var/www/aigc-agent"

echo "🌐 配置 Nginx..."

# 创建 Nginx 配置文件
sudo tee /etc/nginx/sites-available/aigc-agent > /dev/null <<EOF
server {
    listen 80;
    server_name ${DOMAIN} www.${DOMAIN};

    # 前端静态文件
    location / {
        root ${PROJECT_DIR}/dist;
        try_files \$uri \$uri/ /index.html;
        index index.html;
    }

    # 后端 API 代理
    location /api {
        proxy_pass http://localhost:3002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# 启用配置
sudo ln -sf /etc/nginx/sites-available/aigc-agent /etc/nginx/sites-enabled/

# 删除默认配置（可选）
sudo rm -f /etc/nginx/sites-enabled/default

# 测试配置
sudo nginx -t

# 重新加载 Nginx
sudo systemctl reload nginx

echo "✅ Nginx 配置完成！"

