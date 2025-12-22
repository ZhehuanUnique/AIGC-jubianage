# 签名调试指南

## 当前问题

即梦 API 返回 `SignatureDoesNotMatch` 错误，说明签名算法可能有问题。

## 已尝试的修复

1. ✅ 修复了时间戳格式（ISO 8601）
2. ✅ 修复了查询参数格式
3. ✅ 修复了请求头格式
4. ✅ 修复了端点 URL（使用 visual.volcengineapi.com）
5. ✅ 实现了 V4 签名算法

## 可能的问题

1. **Secret Access Key 处理**：
   - 当前：base64 解码后使用
   - 可能需要：直接使用 base64 字符串

2. **Action 和 Version 参数**：
   - 当前：使用 `Action=CVProcess, Version=2022-08-31`
   - 可能需要：不同的 Action 值，或者不需要这些参数

3. **签名密钥生成**：
   - 当前：按照官方示例实现
   - 可能需要：检查是否有其他细节

## 建议

1. 查看即梦 API 的官方文档，确认：
   - 是否需要 Action 和 Version 查询参数
   - 正确的 Action 值是什么
   - Secret Access Key 是否需要 base64 解码

2. 联系即梦 API 技术支持，获取：
   - 正确的签名示例
   - Secret Access Key 的正确使用方式

3. 检查火山引擎控制台，确认：
   - AK/SK 是否正确
   - 是否有其他配置要求

## 测试网址

- 测试页面：http://localhost:8888/test_jimeng_api.html
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

