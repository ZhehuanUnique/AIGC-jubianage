# 一键部署脚本 - Windows PowerShell
# 使用方法：在项目根目录执行 .\一键部署.ps1

$ServerIP = "119.45.121.152"
$ServerUser = "ubuntu"
$RemotePath = "/var/www/aigc-agent"
$Domain = "jubianai.cn"

Write-Host "🚀 开始一键部署到腾讯云服务器..." -ForegroundColor Green
Write-Host "服务器: $ServerIP" -ForegroundColor Cyan
Write-Host "域名: $Domain" -ForegroundColor Cyan
Write-Host ""

# 步骤1：上传安装脚本并安装环境
Write-Host "📦 步骤 1/6: 上传安装脚本..." -ForegroundColor Yellow
scp deploy-to-server.sh "${ServerUser}@${ServerIP}:/tmp/" 2>&1 | Out-Null

Write-Host "📦 步骤 1/6: 在服务器上安装环境（这需要几分钟）..." -ForegroundColor Yellow
ssh "${ServerUser}@${ServerIP}" "chmod +x /tmp/deploy-to-server.sh && bash /tmp/deploy-to-server.sh"

Write-Host "✅ 环境安装完成！" -ForegroundColor Green
Write-Host ""

# 步骤2：上传代码
Write-Host "📤 步骤 2/6: 上传代码到服务器..." -ForegroundColor Yellow
Write-Host "⚠️  这可能需要几分钟，请耐心等待..." -ForegroundColor Yellow

# 检查是否有 tar 命令
if (Get-Command tar -ErrorAction SilentlyContinue) {
    Write-Host "使用 tar 压缩上传（更快）..." -ForegroundColor Cyan
    $tarFile = "deploy-temp.tar.gz"
    
    tar --exclude='node_modules' `
        --exclude='.git' `
        --exclude='dist' `
        --exclude='.env*' `
        --exclude='*.log' `
        -czf $tarFile .
    
    scp $tarFile "${ServerUser}@${ServerIP}:/tmp/"
    ssh "${ServerUser}@${ServerIP}" "cd $RemotePath && tar -xzf /tmp/$tarFile && rm /tmp/$tarFile"
    Remove-Item $tarFile
} else {
    Write-Host "使用 scp 上传（较慢）..." -ForegroundColor Cyan
    ssh "${ServerUser}@${ServerIP}" "mkdir -p $RemotePath"
    
    # 上传主要文件
    $filesToUpload = @(
        "package.json",
        "package-lock.json",
        "vite.config.ts",
        "tsconfig.json",
        "tailwind.config.js",
        "postcss.config.js",
        "index.html"
    )
    
    foreach ($file in $filesToUpload) {
        if (Test-Path $file) {
            scp $file "${ServerUser}@${ServerIP}:$RemotePath/"
        }
    }
    
    # 上传目录
    $dirsToUpload = @("src", "server", "public")
    foreach ($dir in $dirsToUpload) {
        if (Test-Path $dir) {
            scp -r $dir "${ServerUser}@${ServerIP}:$RemotePath/"
        }
    }
}

Write-Host "✅ 代码上传完成！" -ForegroundColor Green
Write-Host ""

# 步骤3：上传部署脚本
Write-Host "📤 步骤 3/6: 上传部署脚本..." -ForegroundColor Yellow
scp deploy-app.sh "${ServerUser}@${ServerIP}:$RemotePath/" 2>&1 | Out-Null
scp setup-nginx.sh "${ServerUser}@${ServerIP}:$RemotePath/" 2>&1 | Out-Null
scp setup-ssl.sh "${ServerUser}@${ServerIP}:$RemotePath/" 2>&1 | Out-Null

Write-Host "✅ 脚本上传完成！" -ForegroundColor Green
Write-Host ""

# 步骤4：提示配置环境变量
Write-Host "⚙️  步骤 4/6: 配置环境变量" -ForegroundColor Yellow
Write-Host "⚠️  重要：请先配置环境变量！" -ForegroundColor Red
Write-Host ""
Write-Host "执行以下命令配置环境变量：" -ForegroundColor Cyan
Write-Host "  ssh ${ServerUser}@${ServerIP}" -ForegroundColor White
Write-Host "  cd $RemotePath/server" -ForegroundColor White
Write-Host "  cp env.example .env" -ForegroundColor White
Write-Host "  nano .env" -ForegroundColor White
Write-Host ""
Write-Host "必须配置的项：" -ForegroundColor Yellow
Write-Host "  - DATABASE_URL (Supabase连接字符串)" -ForegroundColor White
Write-Host "  - JWT_SECRET (使用命令生成: node -e \"console.log(require('crypto').randomBytes(32).toString('hex'))\")" -ForegroundColor White
Write-Host "  - COS_SECRET_ID, COS_SECRET_KEY, COS_BUCKET" -ForegroundColor White
Write-Host ""
$continue = Read-Host "配置完成后，按 Enter 继续部署，或输入 'skip' 跳过（稍后手动部署）"
if ($continue -eq "skip") {
    Write-Host "⏭️  跳过部署，请稍后手动执行部署脚本" -ForegroundColor Yellow
    Write-Host "部署命令: ssh ${ServerUser}@${ServerIP} 'cd $RemotePath && bash deploy-app.sh'" -ForegroundColor Cyan
    exit 0
}

# 步骤5：部署应用
Write-Host "🚀 步骤 5/6: 部署应用..." -ForegroundColor Yellow
ssh "${ServerUser}@${ServerIP}" "cd $RemotePath && chmod +x deploy-app.sh setup-nginx.sh && bash deploy-app.sh"

Write-Host "✅ 应用部署完成！" -ForegroundColor Green
Write-Host ""

# 步骤6：配置 Nginx
Write-Host "🌐 步骤 6/6: 配置 Nginx..." -ForegroundColor Yellow
ssh "${ServerUser}@${ServerIP}" "cd $RemotePath && bash setup-nginx.sh"

Write-Host "✅ Nginx 配置完成！" -ForegroundColor Green
Write-Host ""

# 完成
Write-Host "🎉 部署完成！" -ForegroundColor Green
Write-Host ""
Write-Host "📝 下一步：" -ForegroundColor Yellow
Write-Host "1. 配置 SSL 证书（HTTPS）:" -ForegroundColor Cyan
Write-Host "   ssh ${ServerUser}@${ServerIP}" -ForegroundColor White
Write-Host "   cd $RemotePath && bash setup-ssl.sh" -ForegroundColor White
Write-Host ""
Write-Host "2. 访问网站:" -ForegroundColor Cyan
Write-Host "   http://$Domain" -ForegroundColor White
Write-Host "   https://$Domain (配置SSL后)" -ForegroundColor White
Write-Host ""
Write-Host "3. 检查服务状态:" -ForegroundColor Cyan
Write-Host "   ssh ${ServerUser}@${ServerIP} 'pm2 status'" -ForegroundColor White

