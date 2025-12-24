# 从官方文档获取 req_key

## 📋 请提供以下信息

根据你提供的官方文档，请告诉我文档中明确列出的 req_key 值：

### 1080P-首帧接口文档
**链接**: https://www.volcengine.com/docs/85621/1798092?lang=zh

**请提供**:
- req_key 的值: `?`

### 1080P-首尾帧接口文档  
**链接**: https://www.volcengine.com/docs/85621/1802721?lang=zh

**请提供**:
- req_key 的值: `?`

## 🔍 在文档中查找 req_key 的位置

通常在文档的以下位置可以找到：
1. **请求参数** 部分
2. **接口说明** 部分
3. **请求示例** 中的 `req_key` 字段
4. **参数说明** 表格中

## 💡 当前代码使用的 req_key

**1080P:**
- 首帧: `jimeng_i2v_first_v30_1080p`（推测值）
- 首尾帧: `jimeng_i2v_first_tail_v30_1080p`（推测值）

**720P（已验证）:**
- 首帧: `jimeng_i2v_first_v30`
- 首尾帧: `jimeng_i2v_first_tail_v30`

## 🔧 一旦确认，我会立即更新

一旦你提供正确的 req_key，我会：
1. 更新 `jubianai/backend/api.py` 中的 req_key
2. 更新查询逻辑中的 req_key 列表
3. 提交代码更改

## 📝 或者你可以直接测试

如果你想先测试，可以：
1. 部署当前代码
2. 尝试生成 1080P 视频
3. 如果 req_key 错误，API 会返回错误信息
4. 根据错误信息调整 req_key

