# 如何查看 Vercel 提供的 DNS 记录值

## 📍 查看位置

在 Vercel Dashboard 中添加域名后，DNS 配置信息会显示在 **Settings → Domains** 页面。

---

## 🔍 详细步骤

### 1. 进入项目设置

1. 登录 Vercel Dashboard: https://vercel.com/dashboard
2. 点击你的项目（`AIGC-jubianage` 或类似名称）
3. 点击顶部菜单栏的 **"Settings"**（设置）

### 2. 进入 Domains 页面

1. 在左侧菜单中找到 **"Domains"**（域名）
2. 点击进入

### 3. 添加域名

1. 在 "Domains" 页面，你会看到一个输入框
2. 输入你的域名：`jubianai.cn`
3. 点击 **"Add"**（添加）按钮

### 4. 查看 DNS 配置信息 ⭐

添加域名后，Vercel 会立即显示需要配置的 DNS 记录：

#### 显示位置

在域名列表下方，你会看到类似这样的信息：

```
jubianai.cn
Configuration: Invalid

To configure jubianai.cn, add the following DNS record:

Type: CNAME
Name: @
Value: cname.vercel-dns.com
```

或者：

```
jubianai.cn
Configuration: Invalid

To configure jubianai.cn, add the following DNS record:

Type: A
Name: @
Value: 76.76.21.21
```

#### 信息说明

- **Type（类型）**: DNS 记录类型（通常是 CNAME 或 A）
- **Name（名称）**: 主机记录（通常是 `@` 表示根域名）
- **Value（值）**: 这是你需要复制到域名注册商的记录值

---

## 📸 界面示例

在 Vercel Dashboard 中，你会看到类似这样的界面：

```
┌─────────────────────────────────────────┐
│  Settings > Domains                     │
├─────────────────────────────────────────┤
│                                         │
│  Add Domain                             │
│  ┌─────────────────────────────────┐   │
│  │ jubianai.cn              [Add]  │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ jubianai.cn                     │   │
│  │                                 │   │
│  │ Status: Invalid Configuration   │   │
│  │                                 │   │
│  │ To configure jubianai.cn, add  │   │
│  │ the following DNS record:      │   │
│  │                                 │   │
│  │ Type: CNAME                    │   │
│  │ Name: @                        │   │
│  │ Value: cname.vercel-dns.com    │   │
│  │                                 │   │
│  │ [Copy]                          │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

---

## 🔄 不同情况下的显示

### 情况 1: 使用 CNAME（最常见）

```
Type: CNAME
Name: @
Value: cname.vercel-dns.com
```

**说明**: 
- 这是最常见的配置方式
- 适用于大多数域名注册商
- 配置简单，推荐使用

### 情况 2: 使用 A 记录

```
Type: A
Name: @
Value: 76.76.21.21
```

**说明**:
- 某些域名注册商不支持根域名的 CNAME
- 需要使用 A 记录
- Vercel 会提供具体的 IP 地址

### 情况 3: 同时支持 www 子域名

如果你也想支持 `www.jubianai.cn`，Vercel 可能会显示两条记录：

```
记录 1:
Type: CNAME
Name: @
Value: cname.vercel-dns.com

记录 2:
Type: CNAME
Name: www
Value: cname.vercel-dns.com
```

---

## ✅ 配置状态说明

在域名列表中，你会看到不同的状态：

### 1. Invalid Configuration（配置无效）

```
Status: Invalid Configuration
```

**含义**: DNS 记录还未配置或未生效

**操作**: 按照 Vercel 显示的 DNS 记录值进行配置

### 2. Valid Configuration（配置有效）

```
Status: Valid Configuration
```

**含义**: DNS 记录已正确配置并生效

**操作**: 无需操作，域名已可以使用

### 3. Pending（等待中）

```
Status: Pending
```

**含义**: DNS 记录已配置，等待 DNS 传播生效

**操作**: 等待 10-30 分钟，状态会自动更新

---

## 📋 复制 DNS 记录值

### 方法 1: 手动复制

1. 在 Vercel 显示的 DNS 配置信息中
2. 找到 **"Value"** 字段
3. 手动复制该值（如：`cname.vercel-dns.com`）

### 方法 2: 使用复制按钮

某些情况下，Vercel 会提供 **"Copy"** 按钮：
1. 点击 **"Copy"** 按钮
2. 记录值会被复制到剪贴板
3. 粘贴到域名注册商的 DNS 配置中

---

## 🔧 在域名注册商中配置

### 以阿里云为例：

1. 登录阿里云控制台
2. 进入 **域名** → **域名解析**
3. 找到 `jubianai.cn` 域名
4. 点击 **"添加记录"**
5. 填写信息：
   - **记录类型**: 选择 Vercel 显示的 Type（CNAME 或 A）
   - **主机记录**: 填写 Vercel 显示的 Name（通常是 `@`）
   - **记录值**: 粘贴 Vercel 显示的 Value（如 `cname.vercel-dns.com`）
   - **TTL**: 600（或默认值）
6. 点击 **"确认"**

### 以腾讯云为例：

1. 登录腾讯云控制台
2. 进入 **域名注册** → **我的域名**
3. 找到 `jubianai.cn`，点击 **"解析"**
4. 点击 **"添加记录"**
5. 填写信息（同上）
6. 点击 **"保存"**

---

## ⏱️ 等待生效

配置 DNS 记录后：

1. **返回 Vercel Dashboard**
2. **刷新 Domains 页面**
3. **观察状态变化**:
   - 从 "Invalid Configuration" → "Pending" → "Valid Configuration"
4. **通常需要 10-30 分钟**，最长可能需要 48 小时

---

## 🆘 如果看不到 DNS 配置信息

### 可能的原因：

1. **域名还未添加**
   - 解决：先添加域名 `jubianai.cn`

2. **页面未刷新**
   - 解决：刷新浏览器页面

3. **浏览器缓存问题**
   - 解决：清除浏览器缓存或使用无痕模式

4. **Vercel 界面更新**
   - 解决：查看 Vercel 官方文档或联系支持

---

## 📞 需要帮助？

如果仍然找不到 DNS 配置信息，可以：

1. **查看 Vercel 官方文档**
   - https://vercel.com/docs/concepts/projects/domains

2. **联系 Vercel 支持**
   - 在 Vercel Dashboard 中点击 "Help" 或 "Support"

3. **提供截图**
   - 我可以帮你分析具体的界面情况

---

## 🎯 快速检查清单

- [ ] 已登录 Vercel Dashboard
- [ ] 已进入项目 Settings → Domains
- [ ] 已添加域名 `jubianai.cn`
- [ ] 已看到 DNS 配置信息（Type, Name, Value）
- [ ] 已复制 Value 值
- [ ] 已在域名注册商中配置 DNS 记录
- [ ] 已等待 10-30 分钟
- [ ] 状态已变为 "Valid Configuration"

