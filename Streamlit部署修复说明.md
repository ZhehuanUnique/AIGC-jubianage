# Streamlit Cloud 部署修复说明

## 问题分析

当前情况：
- ✅ `jubianai` 文件夹已经在 `AIGC-jubianage` 仓库中
- ✅ `jubianai/frontend/app.py` 文件存在且已提交
- ❌ Streamlit Cloud 连接的是 `ZhehuanUnique/jubianai` 仓库（单独的仓库）
- ❌ 但实际文件在 `ZhehuanUnique/AIGC-jubianage` 仓库中

## 解决方案

### 方案一：在 Streamlit Cloud 中更改仓库（推荐）

**步骤：**

1. **在 Streamlit Cloud 中编辑应用设置**
   - 进入你的 Streamlit Cloud 应用设置
   - 找到 "Repository" 设置

2. **更改仓库**
   - 将 Repository 从 `ZhehuanUnique/jubianai` 
   - 改为 `ZhehuanUnique/AIGC-jubianage`

3. **确认路径**
   - Main file path: `jubianai/frontend/app.py` ✅（这个路径是正确的）

4. **保存并重新部署**

### 方案二：将 jubianai 内容推送到独立仓库（如果保留独立仓库）

如果你希望保留 `jubianai` 作为独立仓库：

1. **克隆 jubianai 仓库**
   ```bash
   git clone https://github.com/ZhehuanUnique/jubianai.git
   cd jubianai
   ```

2. **复制文件**
   ```bash
   # 从 jubianage 仓库复制 jubianai 文件夹内容
   cp -r ../AIGC-jubianage/jubianai/* .
   ```

3. **提交并推送**
   ```bash
   git add .
   git commit -m "更新 jubianai 应用"
   git push origin main
   ```

4. **在 Streamlit Cloud 中**
   - Repository: `ZhehuanUnique/jubianai`
   - Main file path: `frontend/app.py`（注意：没有 jubianai 前缀）

## 推荐方案

**推荐使用方案一**，因为：
- ✅ 所有代码在一个仓库中，便于管理
- ✅ 不需要维护两个仓库
- ✅ 部署配置更简单

## 操作步骤（方案一）

### 1. 在 Streamlit Cloud 中修改配置

1. 登录 Streamlit Cloud
2. 进入你的应用设置
3. 点击 "Settings" 或 "Edit app"
4. 找到 "Repository" 部分
5. 点击 "Change repository" 或编辑
6. 将仓库改为：`ZhehuanUnique/AIGC-jubianage`
7. Branch: `main`
8. Main file path: `jubianai/frontend/app.py`
9. 保存设置

### 2. 验证文件存在

确保 GitHub 仓库中有以下文件：
- ✅ `jubianai/frontend/app.py`
- ✅ `jubianai/requirements.txt`
- ✅ `jubianai/config.py`
- ✅ `jubianai/backend/api.py`

### 3. 配置环境变量

在 Streamlit Cloud 设置中添加：
- `BACKEND_URL`: 你的后端 API 地址（部署 FastAPI 后获取）
- `ENV`: `production`

## 验证

修改后，Streamlit Cloud 应该能够：
1. ✅ 找到 `jubianai/frontend/app.py` 文件
2. ✅ 成功部署应用
3. ✅ 生成应用地址（例如：`https://jubianai.streamlit.app`）

## 注意事项

- 如果之前有独立的 `jubianai` 仓库，可以保留它（用于其他用途），但 Streamlit Cloud 应该连接 `AIGC-jubianage` 仓库
- 确保 `AIGC-jubianage` 仓库是公开的，或者你的 Streamlit Cloud 账号有访问权限
- 部署后，记得更新主页面的 `JUBIANAI_AGENT_URL` 环境变量

