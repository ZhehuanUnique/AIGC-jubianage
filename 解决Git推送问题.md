# 解决 Git 推送网络问题

## 🔍 问题诊断

从截图看到两个错误：
1. `Recv failure: Connection was reset` - 连接被重置
2. `Failed to connect to github.com port 43` - 无法连接到 GitHub

## 🔧 解决方案

### 方案 1: 使用 SSH 代替 HTTPS（推荐）

如果 HTTPS 连接不稳定，可以改用 SSH：

```bash
# 在 jubianai 目录下
cd jubianai

# 删除现有的 HTTPS 远程仓库
git remote remove origin

# 添加 SSH 远程仓库
git remote add origin git@github.com:ZhehuanUnique/jubianai-backend.git

# 推送
git push -u origin main
```

**注意**：需要先配置 SSH 密钥，参考：https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### 方案 2: 配置 Git 代理（如果使用代理）

```bash
# 设置 HTTP 代理
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy https://proxy.example.com:8080

# 或者只对 GitHub 设置代理
git config --global http.https://github.com.proxy http://proxy.example.com:8080
```

### 方案 3: 增加超时时间

```bash
# 增加 HTTP 超时时间
git config --global http.postBuffer 524288000
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 999999
```

### 方案 4: 使用 GitHub CLI（gh）

如果 Git 推送一直失败，可以使用 GitHub CLI：

```bash
# 安装 GitHub CLI（如果还没有）
# Windows: winget install GitHub.cli

# 登录
gh auth login

# 在 jubianai 目录下推送
cd jubianai
gh repo create jubianai-backend --private --source=. --remote=origin --push
```

### 方案 5: 手动上传（最后手段）

如果所有方法都失败：

1. 在 GitHub 上创建仓库 `jubianai-backend`
2. 在 GitHub 网页上直接上传文件
3. 或者使用 GitHub Desktop 客户端

## ✅ 快速检查

```bash
# 检查远程仓库配置
cd jubianai
git remote -v

# 测试连接
git ls-remote origin

# 如果连接成功，再尝试推送
git push -u origin main
```

## 📝 关于目录名和仓库名

**目录名** (`jubianai`) 和 **GitHub 仓库名** (`jubianai-backend`) **可以不同**，这是完全正常的：

- ✅ 本地目录：`jubianai` - 这是你的项目文件夹名
- ✅ GitHub 仓库：`jubianai-backend` - 这是远程仓库名，更明确表示这是后端服务

如果你想让它们一致，有两个选择：

1. **重命名 GitHub 仓库**（推荐）：
   - 在 GitHub 上进入仓库设置
   - 重命名为 `jubianai`
   - 更新远程地址：`git remote set-url origin https://github.com/ZhehuanUnique/jubianai.git`

2. **保持现状**：
   - 目录名和仓库名不同是常见的做法
   - `jubianai-backend` 更清楚地表明这是后端服务

---

**建议**：先解决网络连接问题，然后再决定是否要统一名称。

