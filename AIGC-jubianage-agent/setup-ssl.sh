#!/bin/bash

# SSL 证书配置脚本
# 在服务器上执行

DOMAIN="jubianai.cn"
EMAIL="your@email.com"  # 请修改为你的邮箱

echo "🔒 配置 SSL 证书..."

# 安装 Certbot
if ! command -v certbot &> /dev/null; then
    sudo apt install certbot python3-certbot-nginx -y
fi

# 获取 SSL 证书
echo "请输入你的邮箱地址（用于接收证书通知）："
read -p "Email: " EMAIL

sudo certbot --nginx -d ${DOMAIN} -d www.${DOMAIN} --email ${EMAIL} --agree-tos --non-interactive

# 测试自动续期
sudo certbot renew --dry-run

echo "✅ SSL 证书配置完成！"
echo "🌐 现在可以通过 https://${DOMAIN} 访问你的网站了！"

