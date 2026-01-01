# Windows PowerShell 脚本 - 上传代码到服务器
# 使用方法：在项目根目录执行 .\upload-to-server.ps1

$ServerIP = "119.45.121.152"
$ServerUser = "ubuntu"
$RemotePath = "/var/www/aigc-agent"

Write-Host "📤 开始上传代码到服务器..." -ForegroundColor Yellow

# 检查是否在项目根目录
if (-not (Test-Path "package.json")) {
    Write-Host "❌ 错误: 请在项目根目录执行此脚本" -ForegroundColor Red
    exit 1
}

# 创建临时目录（排除不需要的文件）
Write-Host "📦 准备上传文件..." -ForegroundColor Yellow

# 使用 scp 上传（排除 node_modules, .git, dist）
$excludePatterns = @(
    "node_modules",
    ".git",
    "dist",
    ".env",
    ".env.local",
    ".env.production",
    "*.log"
)

# 构建 scp 命令
$files = Get-ChildItem -Path . -Recurse -File | Where-Object {
    $exclude = $false
    foreach ($pattern in $excludePatterns) {
        if ($_.FullName -like "*\$pattern\*") {
            $exclude = $true
            break
        }
    }
    -not $exclude
}

Write-Host "📤 上传文件到服务器..." -ForegroundColor Yellow

# 使用 tar 压缩并上传（更高效）
if (Get-Command tar -ErrorAction SilentlyContinue) {
    # 创建临时 tar 文件
    $tarFile = "deploy-temp.tar.gz"
    
    # 排除文件并打包
    tar --exclude='node_modules' `
        --exclude='.git' `
        --exclude='dist' `
        --exclude='.env*' `
        --exclude='*.log' `
        -czf $tarFile .
    
    # 上传并解压
    scp $tarFile "${ServerUser}@${ServerIP}:/tmp/"
    ssh "${ServerUser}@${ServerIP}" "cd $RemotePath && tar -xzf /tmp/$tarFile && rm /tmp/$tarFile"
    
    # 删除临时文件
    Remove-Item $tarFile
    
    Write-Host "✅ 代码上传完成！" -ForegroundColor Green
} else {
    Write-Host "⚠️  tar 命令不可用，使用 scp 逐个上传（可能较慢）..." -ForegroundColor Yellow
    
    # 创建远程目录
    ssh "${ServerUser}@${ServerIP}" "mkdir -p $RemotePath"
    
    # 上传文件
    foreach ($file in $files) {
        $relativePath = $file.FullName.Replace((Get-Location).Path + "\", "").Replace("\", "/")
        $remoteFile = "$RemotePath/$relativePath"
        $remoteDir = Split-Path $remoteFile -Parent
        
        ssh "${ServerUser}@${ServerIP}" "mkdir -p $remoteDir"
        scp $file.FullName "${ServerUser}@${ServerIP}:$remoteFile"
    }
    
    Write-Host "✅ 代码上传完成！" -ForegroundColor Green
}

Write-Host ""
Write-Host "📝 下一步：" -ForegroundColor Yellow
Write-Host "1. 连接到服务器: ssh ${ServerUser}@${ServerIP}" -ForegroundColor Cyan
Write-Host "2. 配置环境变量: cd $RemotePath/server && cp env.example .env && nano .env" -ForegroundColor Cyan
Write-Host "3. 执行部署脚本: cd $RemotePath && bash deploy-app.sh" -ForegroundColor Cyan

