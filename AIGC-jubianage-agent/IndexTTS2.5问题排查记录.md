# IndexTTS2.5 问题排查记录

**日期**: 2025-12-29  
**状态**: 服务已启动，但前端仍无法加载音色列表

---

## ✅ 已完成的配置

### 1. IndexTTS2.5 服务状态
- ✅ 服务已成功启动
- ✅ 运行在 `http://localhost:8000`
- ✅ 健康检查接口正常：`/api/health` 返回 200 OK
- ✅ 音色列表接口正常：`/api/voices` 返回 200 OK，数据格式为数组
- ✅ 模型已加载（GPT、语义模型、S2Mel、BigVGAN）
- ⚠️ BigVGAN CUDA 内核加载失败（已回退到 torch，不影响功能）

### 2. 后端服务状态
- ✅ 后端服务已启动
- ✅ 运行在 `http://localhost:3002`
- ✅ 日志显示：`IndexTTS2.5音色创作API已启动`
- ✅ 数据库连接正常

### 3. 环境变量配置
```env
INDEXTTS_BASE_URL=http://localhost:8000
INDEXTTS_ENABLED=true
INDEXTTS_PATH=F:\IndexTTS2.5
INDEXTTS_TIMEOUT=60000
```

### 4. 代码修复
- ✅ 修复了 `api_server.py` 中的 `lifespan` 未定义错误
- ✅ 修复了后端服务对数组格式响应的处理
- ✅ 添加了更详细的错误日志

---

## ❌ 当前问题

### 问题描述
前端应用在访问音色创作页面时，显示错误：
```
加载音色列表失败,请检查 IndexTTS2.5 服务是否运行
```

### 测试结果
1. **IndexTTS2.5 服务直接访问**：
   - `http://localhost:8000/api/health` ✅ 正常（返回 200）
   - `http://localhost:8000/api/voices` ✅ 正常（返回数组格式数据）

2. **后端服务状态**：
   - 后端服务已重启
   - 日志显示服务已启动
   - 但前端调用 `/api/indextts/voices` 时仍然失败

---

## 🔍 可能的原因

### 1. 后端服务连接问题
- 后端服务可能在 IndexTTS2.5 启动之前启动，需要重启
- 环境变量可能未正确加载
- 网络连接问题（localhost 访问）

### 2. API 响应格式问题
- `/api/voices` 返回的是数组格式：`[{"id":"default",...}]`
- 后端代码已修复支持数组格式，但可能需要重启生效

### 3. 认证/权限问题
- 前端调用需要认证 token
- 后端 API 路由需要 `authenticateToken` 中间件

### 4. CORS 问题
- IndexTTS2.5 API 服务器可能没有设置 CORS 头
- 导致浏览器阻止跨域请求

---

## 📋 待排查事项

### 优先级 1：检查后端服务日志
1. 查看后端服务命令行窗口的完整日志
2. 查找以下错误信息：
   - `IndexTTS2.5 健康检查失败`
   - `获取音色列表失败`
   - `IndexTTS2.5 服务地址`
   - 任何网络连接错误

### 优先级 2：测试后端 API
1. 测试后端健康检查接口：
   ```bash
   curl http://localhost:3002/api/indextts/health
   ```
   （需要认证 token）

2. 测试后端音色列表接口：
   ```bash
   curl http://localhost:3002/api/indextts/voices
   ```
   （需要认证 token）

### 优先级 3：检查前端网络请求
1. 打开浏览器开发者工具（F12）
2. 查看 Network 标签
3. 找到 `/api/indextts/voices` 请求
4. 查看：
   - 请求 URL
   - 请求头（特别是 Authorization）
   - 响应状态码
   - 响应内容

### 优先级 4：检查 IndexTTS2.5 API 服务器
1. 确认服务仍在运行（检查进程）
2. 查看 IndexTTS2.5 服务窗口的日志
3. 确认是否有来自后端的请求日志

---

## 🛠️ 已创建的脚本和文件

### 启动脚本
- `启动IndexTTS2.5-本地服务.bat` - 本地启动脚本
- `启动IndexTTS2.5-新窗口.bat` - 在新窗口启动
- `重启IndexTTS2.5服务.bat` - 重启服务
- `停止IndexTTS2.5服务.bat` - 停止服务

### 配置文件
- `F:\IndexTTS2.5\api_server.py` - API 服务器（已修复）
- `server/services/indexTtsService.js` - 后端服务（已修复）

### 测试脚本
- `检查IndexTTS2.5连接.bat` - 检查服务连接

---

## 📝 下一步操作建议

### 明天继续处理时：

1. **首先检查后端服务日志**
   - 查看后端服务窗口的完整输出
   - 特别关注调用 IndexTTS2.5 时的错误信息

2. **测试后端 API 连接**
   - 使用 Postman 或 curl 测试后端接口
   - 需要先登录获取 token

3. **检查浏览器控制台**
   - 打开开发者工具
   - 查看 Console 和 Network 标签
   - 记录具体的错误信息

4. **验证服务连接**
   - 确认 IndexTTS2.5 服务仍在运行
   - 确认后端服务仍在运行
   - 测试直接访问 IndexTTS2.5 API

5. **如果问题仍然存在**
   - 考虑添加更详细的日志
   - 检查 CORS 配置
   - 检查网络防火墙设置

---

## 🔧 快速测试命令

### 测试 IndexTTS2.5 服务
```bash
# 健康检查
curl http://localhost:8000/api/health

# 音色列表
curl http://localhost:8000/api/voices
```

### 测试后端服务
```bash
# 后端健康检查（不需要认证）
curl http://localhost:3002/health

# IndexTTS2.5 健康检查（需要认证）
curl -H "Authorization: Bearer <token>" http://localhost:3002/api/indextts/health
```

### 检查进程
```bash
# 检查 IndexTTS2.5 进程
netstat -ano | findstr :8000

# 检查后端进程
netstat -ano | findstr :3002
```

---

## 📌 重要提示

1. **服务启动顺序**：
   - 先启动 IndexTTS2.5 服务（等待完全启动）
   - 再启动后端服务
   - 最后启动前端

2. **环境变量**：
   - 确保 `server/.env` 文件存在且配置正确
   - 重启后端服务后环境变量才会生效

3. **日志查看**：
   - IndexTTS2.5 服务窗口会显示所有请求日志
   - 后端服务窗口会显示连接错误（如果有）

---

## 🎯 预期结果

修复后应该：
1. 前端能正常加载音色列表
2. 后端日志显示成功连接到 IndexTTS2.5
3. IndexTTS2.5 服务窗口显示来自后端的请求日志

---

**最后更新**: 2025-12-29  
**下次处理**: 检查后端服务日志和浏览器网络请求

