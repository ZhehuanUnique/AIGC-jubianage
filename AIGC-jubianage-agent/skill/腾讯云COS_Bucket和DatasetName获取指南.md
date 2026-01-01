# 腾讯云 COS Bucket 和 DatasetName 获取指南

本指南详细说明如何获取腾讯云 COS 的存储桶名称（Bucket）和数据集名称（DatasetName）。

## 一、获取存储桶名称（Bucket）

### 步骤 1: 登录腾讯云控制台

1. 访问 [腾讯云控制台](https://console.cloud.tencent.com)
2. 使用您的账号登录

### 步骤 2: 进入 COS 控制台

1. 在控制台首页，搜索 "COS" 或 "对象存储"
2. 点击 **对象存储 COS** 进入控制台
3. 或直接访问：[COS 控制台](https://console.cloud.tencent.com/cos)

### 步骤 3: 查看存储桶列表

1. 在左侧菜单中，点击 **存储桶列表**
2. 您会看到所有已创建的存储桶

### 步骤 4: 获取存储桶名称

存储桶名称格式：`bucket-name-APPID`

**示例：**
- 如果存储桶名称显示为：`my-bucket-1234567890`
- 那么 `my-bucket` 是您设置的名称
- `1234567890` 是您的 APPID（12 位数字）

**在 MCP 配置中使用：**
```json
"--Bucket=my-bucket-1234567890"
```

### 步骤 5: 如果没有存储桶，创建新存储桶

1. 在存储桶列表页面，点击 **创建存储桶** 按钮
2. 填写存储桶信息：
   - **名称**：输入存储桶名称（如 `my-bucket`）
   - **所属地域**：选择存储桶所在的地域（如 `广州`、`北京`）
   - **访问权限**：根据需要选择（私有读写、公有读私有写、公有读写）
   - **其他设置**：根据需要配置
3. 点击 **创建** 按钮
4. 创建成功后，存储桶名称会自动包含 APPID，格式为：`您设置的名称-APPID`

### 步骤 6: 获取 APPID（如果需要单独查看）

1. 访问 [账号信息页面](https://console.cloud.tencent.com/developer)
2. 在 **账号信息** 中可以看到 **APPID**（12 位数字）

---

## 二、获取地域（Region）

在获取存储桶信息时，同时记录存储桶的 **地域**（Region），用于 MCP 配置。

### 查看存储桶地域

1. 在存储桶列表中，找到您的存储桶
2. 在 **地域** 列中可以看到地域信息
3. 常见地域代码对应关系：

| 地域名称 | 地域代码（Region） |
|---------|------------------|
| 广州 | `ap-guangzhou` |
| 北京 | `ap-beijing` |
| 上海 | `ap-shanghai` |
| 成都 | `ap-chengdu` |
| 重庆 | `ap-chongqing` |
| 南京 | `ap-nanjing` |
| 新加坡 | `ap-singapore` |
| 香港 | `ap-hongkong` |
| 首尔 | `ap-seoul` |
| 东京 | `ap-tokyo` |
| 孟买 | `ap-mumbai` |
| 硅谷 | `na-siliconvalley` |
| 弗吉尼亚 | `na-ashburn` |
| 法兰克福 | `eu-frankfurt` |

**在 MCP 配置中使用：**
```json
"--Region=ap-guangzhou"
```

---

## 三、获取数据集名称（DatasetName）

`DatasetName` 是用于 **智能检索 MetaInsight** 功能的数据集名称。这个功能用于文搜图、图搜图等智能检索。

### 步骤 1: 进入数据万象控制台

1. 在腾讯云控制台首页，搜索 "数据万象" 或 "CI"
2. 点击 **数据万象 CI** 进入控制台
3. 或直接访问：[数据万象控制台](https://console.cloud.tencent.com/ci)

### 步骤 2: 进入智能检索

1. 在左侧菜单中，找到 **数据智能** 或 **智能检索**
2. 点击 **MetaInsight** 或 **智能检索**

### 步骤 3: 查看或创建数据集

1. 在数据集列表中，查看已有的数据集
2. 如果没有数据集，点击 **创建数据集**
3. 填写数据集信息：
   - **数据集名称**：输入数据集名称（如 `my-dataset`）
   - **关联存储桶**：选择要关联的 COS 存储桶
   - **其他设置**：根据需要配置
4. 点击 **创建** 按钮

### 步骤 4: 获取数据集名称

创建或选择数据集后，**数据集名称** 就是 `DatasetName` 的值。

**在 MCP 配置中使用：**
```json
"--DatasetName=my-dataset"
```

### 注意事项

1. **DatasetName 是可选的**：如果不需要智能检索功能，可以不设置 `--DatasetName` 参数
2. **数据集需要先创建**：在使用智能检索功能前，需要先在数据万象控制台创建数据集
3. **数据集关联存储桶**：创建数据集时需要关联一个 COS 存储桶

---

## 四、完整配置示例

获取到所有信息后，在 `.cursor/mcp.json` 中配置：

```json
{
  "mcpServers": {
    "tencent-cos": {
      "command": "npx",
      "args": [
        "-y",
        "cos-mcp@latest",
        "--Region=ap-guangzhou",
        "--Bucket=my-bucket-1234567890",
        "--DatasetName=my-dataset",
        "--connectType=stdio"
      ],
      "env": {
        "COS_SECRET_ID": "YOUR_SECRET_ID_HERE",
        "COS_SECRET_KEY": "YOUR_SECRET_KEY_HERE"
      }
    }
  }
}
```

### 配置说明

- `--Region=ap-guangzhou`：替换为您存储桶的实际地域代码
- `--Bucket=my-bucket-1234567890`：替换为您存储桶的实际名称（包含 APPID）
- `--DatasetName=my-dataset`：替换为您创建的数据集名称（如果不需要智能检索，可以删除此参数）
- `COS_SECRET_ID` 和 `COS_SECRET_KEY`：替换为您的腾讯云 API 密钥

---

## 五、快速检查清单

在配置 MCP 之前，确保您已获取以下信息：

- [ ] **Region（地域）**：如 `ap-guangzhou`
- [ ] **Bucket（存储桶名称）**：如 `my-bucket-1234567890`
- [ ] **DatasetName（数据集名称）**：如 `my-dataset`（可选）
- [ ] **SecretId**：如 `YOUR_SECRET_ID_HERE`
- [ ] **SecretKey**：如 `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## 六、相关链接

- [腾讯云控制台](https://console.cloud.tencent.com)
- [COS 控制台](https://console.cloud.tencent.com/cos)
- [数据万象控制台](https://console.cloud.tencent.com/ci)
- [账号信息（查看 APPID）](https://console.cloud.tencent.com/developer)
- [API 密钥管理](https://console.cloud.tencent.com/cam/capi)

---

## 七、常见问题

### Q1: 存储桶名称格式是什么？

**A:** 存储桶名称格式为 `bucket-name-APPID`，其中：
- `bucket-name` 是您设置的名称
- `APPID` 是您的腾讯云账号 ID（12 位数字）

### Q2: 如何知道我的存储桶在哪个地域？

**A:** 在 COS 控制台的存储桶列表中，**地域** 列会显示存储桶所在的地域。

### Q3: DatasetName 是必需的吗？

**A:** 不是必需的。只有在需要使用智能检索功能（文搜图、图搜图）时才需要设置 `DatasetName`。

### Q4: 如何创建数据集？

**A:** 
1. 访问 [数据万象控制台](https://console.cloud.tencent.com/ci)
2. 进入 **智能检索** 或 **MetaInsight**
3. 点击 **创建数据集**
4. 填写信息并关联存储桶

### Q5: 一个存储桶可以关联多个数据集吗？

**A:** 可以。一个存储桶可以关联多个数据集，用于不同的检索场景。

---

## 八、配置验证

配置完成后，按以下步骤验证：

1. **保存配置文件**：编辑 `.cursor/mcp.json` 并保存
2. **重启 Cursor**：完全关闭并重新打开 Cursor
3. **检查 MCP 状态**：在 Cursor 设置中查看 `tencent-cos` 是否显示为绿色（运行中）
4. **测试功能**：尝试询问 AI："列出 COS 存储桶中的文件"

如果遇到问题，请参考：
- [腾讯云 COS MCP 故障排除指南](./腾讯云COS_MCP故障排除.md)

