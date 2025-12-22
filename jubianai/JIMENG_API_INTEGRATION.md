# 即梦 AI API 集成指南

## 📚 官方文档

- **图生视频-首帧接口**：https://www.volcengine.com/docs/85621/1785204?lang=zh
- **图生视频-首尾帧接口**：https://www.volcengine.com/docs/85621/1791184?lang=zh

## ✅ 已实现的功能

### 1. 首尾帧支持

- ✅ 前端支持上传首帧和尾帧图片
- ✅ 自动转换为 base64 格式
- ✅ 实时预览上传的图片
- ✅ 后端 API 支持接收首尾帧参数

### 2. 即梦 API 集成

- ✅ 更新了后端 API 调用格式
- ✅ 支持即梦 API 的请求格式
- ✅ 支持首尾帧参数传递

## 🔧 API 配置

### 环境变量

在 `.env` 文件或环境变量中配置：

```env
# 即梦 API 端点（火山引擎 API 基础地址）
JIMENG_API_ENDPOINT=https://visual.volcengineapi.com

# 或使用旧的配置项（兼容）
SEEDANCE_API_ENDPOINT=https://visual.volcengineapi.com/video_generation/v1/video_generation_720p

# 火山引擎 Access Key ID（即梦 API 使用 AK/SK 认证）
# ⚠️ 请使用您自己的 AK/SK，不要使用示例值
VOLCENGINE_ACCESS_KEY_ID=your_access_key_id_here

# 火山引擎 Secret Access Key（Base64 编码）
VOLCENGINE_SECRET_ACCESS_KEY=your_secret_access_key_here

# 兼容旧配置（可选）
API_KEY=your_api_key_if_needed
```

### 认证方式

即梦 API 使用**火山引擎的 AK/SK 签名认证**，不是简单的 Bearer Token。

代码已实现：
- ✅ HMAC-SHA256 签名算法
- ✅ 标准签名方式（支持完整请求签名）
- ✅ 简化签名方式（备用方案）
- ✅ 自动签名生成和请求头设置

### 请求格式

根据即梦 API 文档，请求格式应该类似：

```json
{
  "req_key": "video_generation_720p",
  "prompt": "视频描述",
  "width": 1280,
  "height": 720,
  "duration": 5,
  "fps": 24,
  "first_frame": "base64_encoded_image",
  "last_frame": "base64_encoded_image",
  "negative_prompt": "负面提示词（可选）",
  "seed": 12345
}
```

## 📋 参数说明

### 必需参数

- `req_key`: API 请求类型（如 "video_generation_720p"）
- `prompt`: 视频描述（提示词）

### 可选参数

- `width`: 视频宽度（默认 1024）
- `height`: 视频高度（默认 576）
- `duration`: 视频时长（秒，默认 5）
- `fps`: 帧率（默认 24）
- `first_frame`: 首帧图片（base64 编码）
- `last_frame`: 尾帧图片（base64 编码）
- `negative_prompt`: 负面提示词
- `seed`: 随机种子

## 🚀 使用步骤

### 1. 配置 API

在 Streamlit 侧边栏或环境变量中配置：
- API Key
- 后端 API 地址

### 2. 上传首尾帧（可选）

- 上传首帧图片：控制视频起始画面
- 上传尾帧图片：控制视频结束画面

### 3. 输入提示词

描述想要生成的视频内容

### 4. 生成视频

点击"生成视频"按钮，系统会：
1. 使用 RAG 增强提示词（如果可用）
2. 调用即梦 API 生成视频
3. 传递首尾帧参数（如果上传了）

## 🔍 注意事项

1. **API 端点**：根据即梦 API 文档确认正确的端点 URL
   - 默认使用：`https://visual.volcengineapi.com`
   - API 路径：`/video_generation/v1/video_generation_720p`
2. **认证方式**：✅ 已实现火山引擎 AK/SK 签名认证
   - 使用 HMAC-SHA256 签名算法
   - 自动生成签名并添加到请求头
3. **请求格式**：根据文档确认请求体的具体格式
   - `req_key`: "video_generation_720p"
   - 首尾帧使用 base64 编码的图片字符串
4. **响应格式**：确认任务 ID 在响应中的字段名
   - 支持多种格式：`task_id`、`taskId`、`data.task_id` 等
5. **Secret Access Key**：确保是 Base64 编码的字符串

## 📝 代码位置

- **前端**：`jubianai/frontend/app.py`
- **后端**：`jubianai/backend/api.py`
- **配置**：`jubianai/config.py`

## 🔗 参考链接

- [即梦 AI 视频生成3.0 720P-图生视频-首帧-接口文档](https://www.volcengine.com/docs/85621/1785204?lang=zh)
- [即梦 AI 视频生成3.0 720P-图生视频-首尾帧-接口文档](https://www.volcengine.com/docs/85621/1791184?lang=zh)

