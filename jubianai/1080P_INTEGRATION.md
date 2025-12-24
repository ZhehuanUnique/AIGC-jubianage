# 即梦AI 1080P 视频生成接入说明

## ✅ 已完成的修改

### 1. 后端 API 修改

#### 1.1 添加 resolution 参数
- 在 `VideoGenerationRequest` 模型中添加了 `resolution` 字段
- 默认值为 `"720p"`，支持 `"720p"` 和 `"1080p"` 两种分辨率

#### 1.2 更新 req_key 选择逻辑
根据分辨率和首尾帧情况选择正确的 req_key：

**720P:**
- 仅首帧: `jimeng_i2v_first_v30`
- 首尾帧: `jimeng_i2v_first_tail_v30`

**1080P:**
- 仅首帧: `jimeng_i2v_first_v30_1080p`
- 首尾帧: `jimeng_i2v_first_tail_v30_1080p`

#### 1.3 更新查询逻辑
在查询任务状态时，会尝试所有可能的 req_key（720P 和 1080P 的组合）

### 2. 前端界面修改

#### 2.1 添加分辨率选择按钮
- 在视频参数区域添加了分辨率选择（720P / 1080P）
- 使用 `st.radio` 组件，水平排列，可以互相切换
- 默认选择 720P

#### 2.2 更新 API 调用
- `generate_video` 函数添加了 `resolution` 参数
- 根据分辨率自动设置视频宽高（1080P: 1920x1080, 720P: 1280x720）

## 📋 1080P req_key 说明

根据即梦AI文档，1080P 的 req_key 可能是：
- `jimeng_i2v_first_v30_1080p`（首帧）
- `jimeng_i2v_first_tail_v30_1080p`（首尾帧）

**⚠️ 重要**: 如果实际文档中的 req_key 不同，请告诉我正确的 req_key，我会更新代码。

## 🔍 需要确认的信息

根据你提供的文档链接，请确认以下信息：

1. **1080P 的 req_key 是否正确？**
   - 当前代码使用: `jimeng_i2v_first_v30_1080p` 和 `jimeng_i2v_first_tail_v30_1080p`
   - 如果文档中的 req_key 不同，请提供正确的值

2. **1080P 的参数限制**
   - frames 是否和 720P 一样（121 或 241）？
   - 是否有其他特殊参数要求？

3. **1080P 的计费**
   - 1080P 的计费是否和 720P 不同？
   - 是否需要特殊权限？

## 🧪 测试步骤

1. **测试 720P 生成**
   - 选择 720P 分辨率
   - 上传首帧（可选）
   - 生成视频
   - 确认使用 `jimeng_i2v_first_v30` 或 `jimeng_i2v_first_tail_v30`

2. **测试 1080P 生成**
   - 选择 1080P 分辨率
   - 上传首帧（可选）
   - 生成视频
   - 确认使用 `jimeng_i2v_first_v30_1080p` 或 `jimeng_i2v_first_tail_v30_1080p`

3. **测试切换功能**
   - 在 720P 和 1080P 之间切换
   - 确认参数正确传递
   - 确认生成的视频分辨率正确

## 📝 相关文档

- 720P-首尾帧: https://www.volcengine.com/docs/85621/1791184?lang=zh
- 1080P-首帧: https://www.volcengine.com/docs/85621/1798092?lang=zh
- 1080P-首尾帧: https://www.volcengine.com/docs/85621/1802721?lang=zh
- SDK使用说明: https://www.volcengine.com/docs/6444/1340578?lang=zh
- HTTP请求示例: https://www.volcengine.com/docs/6444/1390583?lang=zh

## 🔧 如果 req_key 不正确

如果实际的 req_key 与代码中的不同，请告诉我正确的值，我会立即更新：

1. 1080P 首帧的 req_key: `?`
2. 1080P 首尾帧的 req_key: `?`

或者你可以直接查看文档，告诉我正确的 req_key 名称。

