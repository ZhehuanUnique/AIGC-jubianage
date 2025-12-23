# 修复 Vercel 构建错误

## 🔴 错误信息

```
Nuxt build error: Error: [vite:load-fallback] Could not load 
/vercel/path0/frontend-nuxt//assets/css/main.css
```

**问题分析**:
- 路径中有双斜杠 `//assets/css/main.css`
- 文件确实存在，但构建时路径解析错误
- 可能是 Vercel Root Directory 设置导致的路径问题

## ✅ 解决方案

### 方案 1: 检查 Vercel Root Directory 设置（最重要）

在 Vercel Dashboard 中：

1. 进入项目 **Settings**
2. 找到 **General** → **Root Directory**
3. **确认设置为**: `frontend-nuxt`（没有尾部斜杠）
4. 如果显示为 `frontend-nuxt/`，改为 `frontend-nuxt`

### 方案 2: 使用 app.vue 导入 CSS（备选）

如果方案 1 不行，可以在 `app.vue` 中直接导入 CSS：

```vue
<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<style>
@import '~/assets/css/main.css';
</style>
```

### 方案 3: 检查文件是否存在

确保以下文件存在：
- ✅ `frontend-nuxt/assets/css/main.css`
- ✅ `frontend-nuxt/nuxt.config.ts`

### 方案 4: 使用相对路径（如果以上都不行）

修改 `nuxt.config.ts`:

```typescript
css: ['./assets/css/main.css'],
```

## 🔧 立即操作步骤

1. **检查 Vercel Root Directory**
   - 登录 Vercel Dashboard
   - 进入项目 Settings → General
   - 确认 Root Directory 为 `frontend-nuxt`（无尾部斜杠）

2. **重新部署**
   - 在 Vercel Dashboard 中点击 "Redeploy"
   - 或推送新的提交触发自动部署

3. **如果还是失败**
   - 查看完整的构建日志
   - 检查是否有其他错误信息

## 📝 当前配置

- ✅ CSS 文件存在: `frontend-nuxt/assets/css/main.css`
- ✅ nuxt.config.ts 配置: `css: ['~/assets/css/main.css']`
- ⚠️ 需要确认: Vercel Root Directory 设置

## 🎯 最可能的原因

**Root Directory 配置问题** - 这是最常见的原因。如果 Root Directory 设置不正确或有多余的斜杠，会导致路径解析错误。

