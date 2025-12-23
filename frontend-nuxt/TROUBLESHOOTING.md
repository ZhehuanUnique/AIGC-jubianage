# 故障排除指南

## "Failed to fetch" 错误

### 原因

1. **Render 免费实例休眠**
   - Render 免费计划的服务在空闲时会自动休眠
   - 首次请求需要 50 秒左右唤醒服务
   - 这是正常现象，不是错误

2. **网络连接问题**
   - 检查网络连接
   - 确认后端 URL 是否正确：`https://jubianai-backend.onrender.com`

3. **CORS 错误**
   - 后端已配置允许所有来源（`allow_origins=["*"]`）
   - 如果仍有问题，检查浏览器控制台

### 解决方案

#### 1. 等待服务唤醒

如果看到 "Failed to fetch" 错误：
- 等待 50-60 秒
- 再次点击"生成视频"按钮
- 前端已实现自动重试机制（最多 3 次）

#### 2. 检查后端状态

访问后端健康检查端点：
```
https://jubianai-backend.onrender.com/health
```

应该返回：
```json
{"status": "healthy"}
```

#### 3. 查看后端日志

在 Render Dashboard 中查看服务日志，确认：
- 服务是否正在运行
- 是否有错误信息
- 请求是否到达后端

#### 4. 测试 API 端点

使用 curl 测试：
```bash
curl -X POST https://jubianai-backend.onrender.com/api/v1/video/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "测试视频",
    "duration": 5
  }'
```

### 前端重试机制

前端已实现自动重试：
- 最多重试 3 次
- 每次重试间隔递增（2秒、4秒、6秒）
- 超时时间：60秒

### 升级 Render 服务

如果频繁遇到休眠问题，可以考虑：
1. 升级到 Render 付费计划（服务不会休眠）
2. 使用其他平台（如 Railway、Fly.io）

## 其他常见问题

### 1. 视频生成超时

- 5秒视频通常需要 1-3 分钟
- 10秒视频需要 2-5 分钟
- 前端会持续轮询状态，直到完成或超时

### 2. 首尾帧上传失败

- 确保图片格式为 JPG、PNG
- 图片大小建议不超过 5MB
- 检查浏览器控制台的错误信息

### 3. 状态轮询失败

- 检查网络连接
- 确认任务 ID 是否正确
- 查看后端日志中的任务状态

## 调试技巧

### 浏览器控制台

打开浏览器开发者工具（F12），查看：
- Network 标签：查看 API 请求和响应
- Console 标签：查看 JavaScript 错误

### 后端日志

在 Render Dashboard 中：
1. 进入服务页面
2. 点击 "Logs" 标签
3. 查看实时日志

### 前端调试

在 `stores/video.ts` 中添加日志：
```typescript
console.log('API Request:', params)
console.log('API Response:', response)
```


