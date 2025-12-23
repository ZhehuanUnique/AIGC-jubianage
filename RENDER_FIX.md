# Render 部署修复指南

## 问题
错误：`No module named uvicorn`

## 解决方案

### 在 Render Dashboard 中手动更新配置

1. **进入服务设置**
   - 在 Render Dashboard 中找到 `jubianai-backend` 服务
   - 点击服务名称进入详情页
   - 点击 "Settings" 标签

2. **更新 Build Command**
   ```
   pip install --upgrade pip && pip install -r jubianai/requirements.txt
   ```

3. **更新 Start Command**
   尝试以下三种方式之一：

   **方式 1（推荐）：**
   ```
   uvicorn jubianai.backend.api:app --host 0.0.0.0 --port $PORT
   ```

   **方式 2（如果方式 1 不行）：**
   ```
   python -m uvicorn jubianai.backend.api:app --host 0.0.0.0 --port $PORT
   ```

   **方式 3（如果前两种都不行）：**
   ```
   /opt/render/project/src/.venv/bin/uvicorn jubianai.backend.api:app --host 0.0.0.0 --port $PORT
   ```

4. **清除构建缓存**
   - 在 "Manual Deploy" 下拉菜单中选择 "Clear build cache & deploy"
   - 这会清除旧的构建缓存并重新构建

5. **保存并部署**
   - 点击 "Save Changes"
   - 或者点击 "Manual Deploy" → "Deploy latest commit"

## 验证

部署成功后，访问：
- 健康检查：`https://jubianai-backend.onrender.com/health`
- API 文档：`https://jubianai-backend.onrender.com/docs`

## 如果仍然失败

检查构建日志，确认：
1. `uvicorn` 是否在依赖安装列表中
2. 构建是否成功完成
3. 虚拟环境路径是否正确


