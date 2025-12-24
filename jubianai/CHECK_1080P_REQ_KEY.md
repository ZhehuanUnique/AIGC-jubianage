# 1080P req_key 确认指南

## 📋 需要确认的信息

根据你提供的官方文档，我需要确认 1080P 的正确 req_key：

### 文档链接
- 1080P-首帧: https://www.volcengine.com/docs/85621/1798092?lang=zh
- 1080P-首尾帧: https://www.volcengine.com/docs/85621/1802721?lang=zh

### 当前代码使用的 req_key

**1080P:**
- 首帧: `jimeng_i2v_first_v30_1080p`
- 首尾帧: `jimeng_i2v_first_tail_v30_1080p`

## 🔍 如何确认

### 方法 1: 查看文档中的 req_key 字段

在官方文档中查找：
1. 打开文档链接
2. 查找 "req_key" 或 "请求参数" 部分
3. 确认 1080P 接口的实际 req_key 值

### 方法 2: 查看请求示例

文档中通常会有请求示例，查看示例中的 `req_key` 字段值。

### 方法 3: 查看接口说明

文档的接口说明部分通常会明确列出 req_key 的值。

## 💡 可能的命名规律

根据 720P 的命名规律：
- 720P 首帧: `jimeng_i2v_first_v30`
- 720P 首尾帧: `jimeng_i2v_first_tail_v30`

1080P 可能是：
- `jimeng_i2v_first_v30_1080p` 或
- `jimeng_i2v_first_v30_1080` 或
- `jimeng_i2v_first_v30_hd` 或
- 其他命名方式

## 🔧 如果 req_key 不同

如果文档中的实际 req_key 与代码中的不同，请告诉我：

1. **1080P 首帧的 req_key**: `?`
2. **1080P 首尾帧的 req_key**: `?`

我会立即更新代码。

## 📝 临时方案

如果暂时无法确认，可以：
1. 先测试 720P 功能（确保正常）
2. 尝试使用当前的 req_key 测试 1080P
3. 如果报错，根据错误信息调整

错误信息通常会提示正确的 req_key 或参数名称。

