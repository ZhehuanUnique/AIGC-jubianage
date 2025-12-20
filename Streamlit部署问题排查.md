# Streamlit Cloud 部署问题排查

## 当前状态

- ✅ 文件已提交到本地：`jubianai/frontend/app.py`
- ✅ 文件在 Git 中：已确认
- ❌ Streamlit Cloud 找不到文件

## 可能的原因

### 1. 文件未推送到 GitHub（最可能）

**检查：**
```bash
# 检查远程仓库是否有文件
git ls-remote --heads origin main
```

**解决：**
```bash
# 确保所有文件已推送
git push origin main
```

### 2. GitHub 同步延迟

有时 GitHub 需要几分钟同步，等待后重试。

### 3. 路径问题

Streamlit Cloud 可能需要：
- 路径：`jubianai/frontend/app.py` ✅
- 或者尝试：`frontend/app.py`（如果 Streamlit 在 jubianai 目录下运行）

### 4. 分支问题

确认：
- Branch: `main` ✅
- 不是 `master` 或其他分支

## 快速解决方案

### 方案 A：确保文件已推送

```bash
# 1. 检查当前状态
git status

# 2. 如果有未提交的更改
git add .
git commit -m "确保 jubianai 文件已提交"

# 3. 推送到 GitHub
git push origin main

# 4. 等待 2-3 分钟，让 GitHub 同步

# 5. 在 Streamlit Cloud 中点击 "Redeploy"
```

### 方案 B：临时测试 - 将 app.py 移到根目录

如果还是找不到，可以临时测试：

```bash
# 1. 复制文件到根目录（仅用于测试）
cp jubianai/frontend/app.py streamlit_app.py

# 2. 提交
git add streamlit_app.py
git commit -m "临时：添加根目录 app 文件用于测试"
git push origin main

# 3. 在 Streamlit Cloud 中
# Main file path: streamlit_app.py

# 4. 测试成功后，可以删除这个文件，改回原路径
```

### 方案 C：使用独立仓库（如果必须）

如果集成方案有问题，可以：

1. **将 jubianai 推送到独立仓库**
   ```bash
   # 在 jubianai 目录下
   cd jubianai
   git init
   git remote add origin https://github.com/ZhehuanUnique/jubianai.git
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```

2. **在 Streamlit Cloud 中**
   - Repository: `ZhehuanUnique/jubianai`
   - Main file path: `frontend/app.py`（注意：没有 jubianai 前缀）

## 推荐操作步骤

1. **首先尝试推送**
   ```bash
   git push origin main
   ```

2. **等待 3-5 分钟**

3. **在 Streamlit Cloud 中点击 "Redeploy" 或 "Deploy"**

4. **如果还是不行，检查 GitHub 网页**
   - 访问：https://github.com/ZhehuanUnique/AIGC-jubianage
   - 确认能看到 `jubianai/frontend/app.py` 文件

5. **如果 GitHub 上有文件但 Streamlit 还是找不到**
   - 尝试清除 Streamlit Cloud 缓存
   - 或者联系 Streamlit 支持

## 验证清单

- [ ] 文件在本地存在：`jubianai/frontend/app.py`
- [ ] 文件已提交到 Git：`git log -- jubianai/frontend/app.py`
- [ ] 文件已推送到 GitHub：在 GitHub 网页上能看到
- [ ] Streamlit Cloud 仓库设置正确：`ZhehuanUnique/AIGC-jubianage`
- [ ] 分支设置正确：`main`
- [ ] 路径设置正确：`jubianai/frontend/app.py`

