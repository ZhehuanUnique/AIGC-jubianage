# 即梦 API 配置说明

## 环境变量配置

### Vercel 环境变量配置

1. 登录 Vercel Dashboard
2. 进入项目 `jubianai` 的设置页面
3. 在 "Environment Variables" 中添加以下变量：

```
JIMENG_ACCESS_KEY_ID=你的即梦AccessKeyId
JIMENG_SECRET_ACCESS_KEY=你的即梦SecretAccessKey
JIMENG_API_ENDPOINT=https://visual.volcengineapi.com
```

### Streamlit Cloud 环境变量配置

1. 登录 Streamlit Cloud Dashboard
2. 进入应用设置页面
3. 在 "Secrets" 中添加以下配置：

```toml
[secrets]
JIMENG_ACCESS_KEY_ID = "你的即梦AccessKeyId"
JIMENG_SECRET_ACCESS_KEY = "你的即梦SecretAccessKey"
JIMENG_API_ENDPOINT = "https://visual.volcengineapi.com"
BACKEND_URL = "https://jubianai.vercel.app"
```

## 本地开发配置

在 `jubianai` 目录下创建 `.env` 文件：

```env
JIMENG_ACCESS_KEY_ID=你的即梦AccessKeyId
JIMENG_SECRET_ACCESS_KEY=你的即梦SecretAccessKey
JIMENG_API_ENDPOINT=https://visual.volcengineapi.com
BACKEND_URL=http://localhost:8000
```

## 使用说明

### 前端使用

1. 打开 Streamlit 应用
2. 在侧边栏选择服务提供商为 "jimeng"
3. 输入即梦 API 密钥（如果未在环境变量中配置）
4. 输入视频描述和参数
5. 点击"生成视频"按钮

### API 调用

#### 生成视频

```bash
curl -X POST https://jubianai.vercel.app/api/v1/video/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "一个美丽的日落场景",
    "width": 1024,
    "height": 576,
    "duration": 5,
    "fps": 24,
    "provider": "jimeng",
    "jimeng_access_key_id": "你的即梦AccessKeyId",
    "jimeng_secret_access_key": "你的即梦SecretAccessKey"
  }'
```

#### 查询状态

```bash
curl "https://jubianai.vercel.app/api/v1/video/status/{task_id}?provider=jimeng"
```

## 注意事项

1. **API 密钥安全**：请勿在代码中硬编码 API 密钥，始终使用环境变量
2. **API 端点**：如果即梦 API 的实际端点不同，请更新 `JIMENG_API_ENDPOINT` 环境变量
3. **签名算法**：当前实现的签名算法可能需要根据即梦 API 文档进行调整
4. **错误处理**：如果遇到 API 调用错误，请检查：
   - API 密钥是否正确
   - API 端点是否正确
   - 签名算法是否符合即梦 API 的要求

