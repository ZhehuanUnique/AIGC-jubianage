# 即梦 API Access Denied (50400) 错误修复指南

## 错误信息
```
请求失败: 视频生成失败:调用即梦API失败: 
b'{"code":50400,"data":null,"message":"Access Denied: Access Denied", 
"request_id":"20251224134611E024A64B7B1C73D6622B","status":50400,"time_elapsed":"129.115µs"}'
```

## 错误原因
状态码 `50400` 表示"Access Denied"，通常由以下原因导致：

1. **API 密钥（AK/SK）未配置或配置错误**
2. **API 密钥没有权限访问即梦 API 服务**
3. **API 密钥已过期或被禁用**
4. **签名认证失败**（SDK 自动处理，但密钥错误会导致签名失败）

## 解决步骤

### 1. 检查环境变量配置

确保后端服务已正确配置以下环境变量：

```bash
VOLCENGINE_ACCESS_KEY_ID=your_access_key_id_here
VOLCENGINE_SECRET_ACCESS_KEY=your_secret_access_key_here
JIMENG_API_ENDPOINT=https://visual.volcengineapi.com
```

### 2. 验证 API 密钥

#### 2.1 检查密钥是否正确
- 登录 [火山引擎控制台](https://console.volcengine.com/)
- 进入 **访问控制** > **密钥管理**
- 确认 `VOLCENGINE_ACCESS_KEY_ID` 和 `VOLCENGINE_SECRET_ACCESS_KEY` 是否正确

#### 2.2 检查密钥权限
- 确认该密钥有权限访问 **视觉智能（Visual）** 服务
- 确认该密钥有权限调用 **即梦 API**（视频生成服务）

### 3. 检查 API 密钥状态

- 确认密钥**未过期**
- 确认密钥**未被禁用**
- 如果密钥已过期，请创建新的密钥对

### 4. 验证 API 服务开通

- 登录 [火山引擎控制台](https://console.volcengine.com/)
- 进入 **视觉智能（Visual）** > **即梦 API**
- 确认服务已**开通**且**可用**
- 检查账户余额是否充足（如果按量计费）

### 5. 测试 API 密钥

可以使用以下 Python 脚本测试 API 密钥是否有效：

```python
import os
from volcengine.visual.VisualService import VisualService

# 设置你的 AK/SK
access_key_id = os.getenv("VOLCENGINE_ACCESS_KEY_ID", "your_access_key_id")
secret_access_key = os.getenv("VOLCENGINE_SECRET_ACCESS_KEY", "your_secret_access_key")

# 创建服务实例
service = VisualService()
service.set_ak(access_key_id)
service.set_sk(secret_access_key)

# 测试调用（使用一个简单的 req_key）
try:
    params = {
        "req_key": "jimeng_i2v_first_v30",
        "prompt": "测试提示词",
        "frames": 121,
        "seed": -1,
        "binary_data_base64": []  # 这里需要实际的图片 base64
    }
    response = service.cv_sync2async_submit_task(params)
    print("API 调用成功:", response)
except Exception as e:
    print("API 调用失败:", str(e))
    if "Access Denied" in str(e) or "50400" in str(e):
        print("❌ 认证失败：请检查 AK/SK 是否正确，是否有权限访问即梦 API")
    else:
        print("❌ 其他错误：", str(e))
```

### 6. 检查后端服务配置

#### 6.1 本地开发环境
在项目根目录创建 `.env` 文件：

```bash
VOLCENGINE_ACCESS_KEY_ID=your_access_key_id_here
VOLCENGINE_SECRET_ACCESS_KEY=your_secret_access_key_here
JIMENG_API_ENDPOINT=https://visual.volcengineapi.com
```

#### 6.2 部署环境（Railway/Render/Vercel）
在部署平台的环境变量设置中添加：
- `VOLCENGINE_ACCESS_KEY_ID`
- `VOLCENGINE_SECRET_ACCESS_KEY`
- `JIMENG_API_ENDPOINT`（可选，默认值已设置）

### 7. 常见问题排查

#### 问题 1：环境变量未生效
**症状**：代码中读取到的环境变量为空

**解决**：
- 确认环境变量名称正确（区分大小写）
- 重启后端服务使环境变量生效
- 检查 `.env` 文件是否在正确位置

#### 问题 2：密钥格式错误
**症状**：密钥包含多余空格或换行符

**解决**：
- 复制密钥时确保没有多余空格
- 如果密钥包含换行符，需要去除

#### 问题 3：服务未开通
**症状**：即使密钥正确，仍然返回 Access Denied

**解决**：
- 登录火山引擎控制台，确认即梦 API 服务已开通
- 检查账户状态和余额

#### 问题 4：区域限制
**症状**：某些区域可能无法访问即梦 API

**解决**：
- 确认 API 端点 `https://visual.volcengineapi.com` 可访问
- 检查网络连接和防火墙设置

### 8. 调试建议

#### 8.1 启用详细日志
在后端代码中添加日志输出，查看实际使用的密钥：

```python
import os
print(f"VOLCENGINE_ACCESS_KEY_ID: {os.getenv('VOLCENGINE_ACCESS_KEY_ID', 'NOT SET')[:10]}...")
print(f"VOLCENGINE_SECRET_ACCESS_KEY: {os.getenv('VOLCENGINE_SECRET_ACCESS_KEY', 'NOT SET')[:10]}...")
```

#### 8.2 检查后端响应
查看后端返回的完整错误信息，确认是认证问题还是其他问题。

### 9. 联系支持

如果以上步骤都无法解决问题，可以：

1. **查看火山引擎文档**：
   - [即梦 API 文档](https://www.volcengine.com/docs/85621?lang=zh)
   - [API 认证文档](https://www.volcengine.com/docs/6444/1340578?lang=zh)

2. **联系火山引擎技术支持**：
   - 提供 `request_id`（错误信息中的 `request_id`）
   - 提供错误详情和时间戳

## 快速检查清单

- [ ] 环境变量 `VOLCENGINE_ACCESS_KEY_ID` 已设置
- [ ] 环境变量 `VOLCENGINE_SECRET_ACCESS_KEY` 已设置
- [ ] 密钥格式正确（无多余空格）
- [ ] 密钥未过期且未被禁用
- [ ] 密钥有权限访问即梦 API
- [ ] 即梦 API 服务已开通
- [ ] 后端服务已重启（使环境变量生效）
- [ ] 网络连接正常

## 相关文件

- `jubianai/config.py` - 配置文件，读取环境变量
- `jubianai/backend/api.py` - API 接口，使用 AK/SK 调用即梦 API
- `jubianai/backend/volcengine_sdk_helper.py` - 火山引擎 SDK 封装

