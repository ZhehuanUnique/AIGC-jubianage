# Git 推送失败问题排查

## 错误信息
```
fatal: unable to access 'https://github.com/ZhehuanUnique/AIGC-jubianage.git/': 
Failed to connect to github.com port 443 after 21035 ms: Could not connect to server
```

## 可能的原因

1. **网络连接问题** - 无法连接到 GitHub
2. **代理设置问题** - 需要配置代理但未配置
3. **防火墙阻止** - 本地防火墙阻止了连接
4. **DNS 解析问题** - 无法解析 github.com

## 解决方案

### 方案 1: 检查网络连接

```powershell
# 测试 GitHub 连接
Test-NetConnection github.com -Port 443

# 如果失败，尝试 ping
ping github.com
```

### 方案 2: 配置 Git 代理（如果需要）

如果你在使用代理，需要配置 Git 使用代理：

```powershell
# HTTP/HTTPS 代理
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy https://proxy.example.com:8080

# 如果使用 SOCKS5 代理
git config --global http.proxy socks5://127.0.0.1:1080
git config --global https.proxy socks5://127.0.0.1:1080

# 查看当前代理配置
git config --global --get http.proxy
git config --global --get https.proxy

# 取消代理配置（如果不需要）
git config --global --unset http.proxy
git config --global --unset https.proxy
```

### 方案 3: 使用 SSH 代替 HTTPS

如果 HTTPS 连接有问题，可以切换到 SSH：

```powershell
# 查看当前远程 URL
git remote -v

# 切换到 SSH（需要先配置 SSH 密钥）
git remote set-url origin git@github.com:ZhehuanUnique/AIGC-jubianage.git

# 验证
git remote -v
```

**注意**: 使用 SSH 需要先配置 SSH 密钥，参考：https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### 方案 4: 增加超时时间

```powershell
# 增加 HTTP 超时时间
git config --global http.postBuffer 524288000
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 999999
```

### 方案 5: 使用 GitHub CLI（如果已安装）

```powershell
# 如果安装了 GitHub CLI
gh auth login
gh repo sync
```

### 方案 6: 稍后重试

如果是临时网络问题，可以：
1. 等待几分钟后重试
2. 检查网络连接
3. 尝试使用移动热点或其他网络

## 快速检查清单

- [ ] 检查网络连接是否正常
- [ ] 测试能否访问 https://github.com
- [ ] 检查是否需要配置代理
- [ ] 尝试使用 SSH 代替 HTTPS
- [ ] 增加 Git 超时时间
- [ ] 稍后重试

## 临时解决方案

如果急需部署，可以：

1. **手动在 GitHub 网页上创建文件**（不推荐，但可行）
2. **使用 GitHub Desktop**（如果有安装）
3. **等待网络恢复后推送**

## 验证修复

修复后，尝试：
```powershell
git push origin main
```

如果成功，应该看到：
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
...
To https://github.com/ZhehuanUnique/AIGC-jubianage.git
   xxxxx..xxxxx  main -> main
```


