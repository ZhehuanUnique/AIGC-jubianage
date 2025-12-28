# 配置 SSH 密钥连接 GitHub

## 🔑 检查是否已有 SSH 密钥

运行以下命令检查：

```bash
# 检查 SSH 密钥是否存在
Test-Path $env:USERPROFILE\.ssh\id_rsa.pub

# 如果返回 True，说明已有密钥
# 如果返回 False，需要生成新密钥
```

## 📝 如果没有 SSH 密钥，生成新密钥

### 步骤 1: 生成 SSH 密钥

```bash
# 生成 SSH 密钥（替换为你的 GitHub 邮箱）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 或者使用 RSA（如果 ed25519 不支持）
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

**提示**：
- 按 Enter 使用默认文件位置
- 可以设置密码（推荐）或直接按 Enter 跳过

### 步骤 2: 启动 SSH 代理

```bash
# 启动 ssh-agent
Start-Service ssh-agent

# 或者
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
```

### 步骤 3: 添加 SSH 密钥到 ssh-agent

```bash
# 添加密钥
ssh-add $env:USERPROFILE\.ssh\id_rsa

# 或者 ed25519
ssh-add $env:USERPROFILE\.ssh\id_ed25519
```

### 步骤 4: 复制公钥

```bash
# 显示公钥内容
Get-Content $env:USERPROFILE\.ssh\id_rsa.pub

# 或者 ed25519
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
```

**复制输出的内容**（从 `ssh-rsa` 或 `ssh-ed25519` 开始到邮箱结束）

### 步骤 5: 添加到 GitHub

1. 登录 GitHub
2. 点击右上角头像 → **Settings**
3. 左侧菜单选择 **SSH and GPG keys**
4. 点击 **New SSH key**
5. **Title**: 输入一个描述（如 "My Windows PC"）
6. **Key**: 粘贴刚才复制的公钥
7. 点击 **Add SSH key**

### 步骤 6: 测试连接

```bash
# 测试 GitHub SSH 连接
ssh -T git@github.com

# 如果成功，会看到：
# Hi ZhehuanUnique! You've successfully authenticated, but GitHub does not provide shell access.
```

## 🔄 更新 Git 远程仓库为 SSH

### 对于 jubianai 目录

```bash
cd jubianai

# 更新远程仓库地址为 SSH
git remote set-url origin git@github.com:ZhehuanUnique/jubianai-backend.git

# 验证
git remote -v
```

### 对于 doubao-rag 目录（稍后）

```bash
cd doubao-rag

# 更新远程仓库地址为 SSH
git remote set-url origin git@github.com:ZhehuanUnique/doubao-rag-service.git

# 验证
git remote -v
```

## 🚀 推送代码

配置完成后，就可以推送了：

```bash
cd jubianai
git push -u origin main
```

## ⚠️ 常见问题

### 问题 1: Permission denied (publickey)

**原因**: SSH 密钥未正确配置

**解决**:
1. 确认公钥已添加到 GitHub
2. 确认私钥已添加到 ssh-agent: `ssh-add ~/.ssh/id_rsa`
3. 测试连接: `ssh -T git@github.com`

### 问题 2: ssh-agent 未启动

**解决**:
```bash
Start-Service ssh-agent
ssh-add $env:USERPROFILE\.ssh\id_rsa
```

### 问题 3: 多个 SSH 密钥

如果有多個密钥，可以配置 `~/.ssh/config`:

```
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa
```

## 📚 参考文档

- [GitHub SSH 文档](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [生成新的 SSH 密钥](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

---

**最后更新**: 2025-12-28

