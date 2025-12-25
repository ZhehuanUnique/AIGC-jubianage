# 分辨率切换功能调试指南

## 🔍 问题排查

如果无法切换 720P/1080P，请按以下步骤排查：

### 1. 检查代码是否已部署

**检查方法**：
1. 打开浏览器开发者工具（F12）
2. 查看 Network 标签
3. 刷新页面
4. 查看加载的 JavaScript 文件
5. 搜索 `resolution` 或 `720p`，确认代码是否包含最新更改

**如果代码未更新**：
- 检查 Vercel 部署状态
- 确认代码已推送到 GitHub
- 等待 Vercel 重新部署完成

### 2. 清除浏览器缓存

**方法 1：硬刷新**
- Windows/Linux: `Ctrl + Shift + R` 或 `Ctrl + F5`
- Mac: `Cmd + Shift + R`

**方法 2：清除缓存**
1. 打开开发者工具（F12）
2. 右键点击刷新按钮
3. 选择"清空缓存并硬性重新加载"

### 3. 检查按钮是否显示

**检查方法**：
1. 打开浏览器开发者工具（F12）
2. 使用元素选择器（Ctrl+Shift+C）
3. 查看控制栏区域
4. 确认是否有 720P 和 1080P 按钮

**如果按钮不存在**：
- 检查控制台是否有 JavaScript 错误
- 检查 Vue 组件是否正确渲染

### 4. 检查控制台错误

**检查方法**：
1. 打开浏览器开发者工具（F12）
2. 查看 Console 标签
3. 查看是否有红色错误信息

**常见错误**：
- `resolutions is not defined` - 变量未定义
- `resolution is not defined` - 变量未定义
- Vue 渲染错误

### 5. 检查网络请求

**检查方法**：
1. 打开浏览器开发者工具（F12）
2. 切换到 Network 标签
3. 点击分辨率按钮
4. 生成视频
5. 查看请求的 payload，确认是否包含 `resolution` 参数

**预期结果**：
```json
{
  "prompt": "...",
  "duration": 5,
  "resolution": "720p" 或 "1080p",
  ...
}
```

## 🔧 手动测试

### 测试 1: 检查变量定义

在浏览器控制台运行：
```javascript
// 检查 Vue 实例
const app = document.querySelector('#__nuxt')
console.log('Vue app:', app)
```

### 测试 2: 检查按钮点击事件

1. 打开开发者工具
2. 选择 Elements 标签
3. 找到分辨率按钮
4. 检查是否有 `@click` 事件绑定

### 测试 3: 检查响应式数据

在 Vue DevTools 中：
1. 安装 Vue DevTools 浏览器扩展
2. 打开 Vue DevTools
3. 查看组件状态
4. 检查 `resolution` 变量的值

## 🐛 可能的问题和解决方案

### 问题 1: 按钮不显示

**原因**：
- CSS 样式问题
- 按钮被其他元素遮挡
- Vue 组件未正确渲染

**解决方案**：
1. 检查 CSS 样式
2. 检查 z-index
3. 检查 Vue 组件是否正确导入

### 问题 2: 点击无反应

**原因**：
- 事件绑定失败
- JavaScript 错误阻止执行
- Vue 响应式系统问题

**解决方案**：
1. 检查控制台错误
2. 检查事件绑定
3. 检查 Vue 响应式数据

### 问题 3: 切换后不生效

**原因**：
- 变量未正确更新
- API 请求未包含 resolution 参数
- 后端未正确处理

**解决方案**：
1. 检查变量值是否正确更新
2. 检查网络请求 payload
3. 检查后端日志

## 📝 代码检查清单

确认以下代码是否正确：

### 1. 变量定义（第 353-354 行）
```typescript
const resolution = ref<'720p' | '1080p'>('720p')
const resolutions: ('720p' | '1080p')[] = ['720p', '1080p']
```

### 2. 按钮模板（第 254-267 行）
```vue
<button
  v-for="res in resolutions"
  :key="res"
  @click="resolution = res"
  ...
>
  {{ res.toUpperCase() }}
</button>
```

### 3. API 调用（第 611 行）
```typescript
resolution: resolution.value,
```

## 🚀 快速修复

如果以上方法都不行，尝试：

1. **重新部署**：
   - 在 Vercel 中手动触发重新部署
   - 或推送一个空提交触发部署

2. **检查部署日志**：
   - 查看 Vercel 部署日志
   - 确认构建是否成功
   - 检查是否有编译错误

3. **回滚测试**：
   - 如果之前版本正常，检查差异
   - 确认更改是否正确应用

## 📞 如果仍然无法解决

请提供以下信息：
1. 浏览器控制台的错误信息
2. 网络请求的 payload
3. Vue DevTools 中的组件状态
4. 按钮是否显示（截图）


