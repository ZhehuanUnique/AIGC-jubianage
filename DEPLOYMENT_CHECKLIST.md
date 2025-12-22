# Vercel 部署检查清单

## 当前问题
静态文件（index.html, styles.css, main.js）返回 404，说明文件没有被部署。

## 已完成的检查
- ✅ Root Directory 设置为空（正确）
- ✅ 文件已提交到 Git 仓库
- ✅ vercel.json 配置已更新

## 需要检查的步骤

### 1. 检查 Vercel 构建日志
在 Vercel Dashboard → Deployments → 最新部署 → Build Logs：

**查找以下信息：**
- [ ] 是否显示 "Uploading static files" 或 "Uploading build outputs"
- [ ] 是否有任何关于静态文件的错误或警告
- [ ] 构建是否成功完成（Build Complete）

**如果构建日志中没有提到静态文件：**
这说明 Vercel 在使用 `builds` 配置时，没有自动包含根目录的静态文件。

### 2. 解决方案 A：移动 API 到标准位置（推荐）

如果构建日志确认静态文件没有被上传，可以尝试：

1. 在根目录创建 `api` 目录
2. 将 `jubianai/api/index.py` 复制或移动到 `api/index.py`
3. 更新 `vercel.json`，移除 `builds` 配置，让 Vercel 自动检测
4. 这样 Vercel 会自动识别 API 路由，同时也会自动部署静态文件

### 3. 解决方案 B：使用 public 目录

1. 创建 `public` 目录
2. 将静态文件移动到 `public` 目录
3. 更新 `vercel.json` 配置

### 4. 解决方案 C：检查项目设置

在 Vercel 项目设置中：
- [ ] "Include files outside the root directory" 已启用（已确认）
- [ ] 检查是否有其他忽略文件的配置

## 下一步行动

**请先检查 Vercel 构建日志，然后告诉我：**
1. 构建日志中是否提到静态文件？
2. 是否有任何错误或警告？
3. 构建是否成功完成？

根据构建日志的结果，我们可以确定下一步的解决方案。

