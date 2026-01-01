# IndexTTS2.5 本地启动指南

## 快速启动

### 方式一：使用 API 服务器（推荐）

1. **直接运行启动脚本**：
   ```bash
   启动IndexTTS2.5-本地服务.bat
   ```

2. **或者使用 IndexTTS2.5 目录中的脚本**：
   ```bash
   F:\IndexTTS2.5\start_api_server.bat
   ```

### 方式二：使用原始 WebUI（带界面）

1. **运行原始启动脚本**：
   ```bash
   F:\IndexTTS2.5\一键启动IndexTTS2.5.bat
   ```
   注意：这会启动 Web UI（端口 7866），不是 API 服务

2. **如果需要 API 接口，使用命令行启动并指定端口**：
   ```bash
   cd F:\IndexTTS2.5
   python webui.py --port 8000 --host 0.0.0.0
   ```

## 配置环境变量

在 `server/.env` 文件中确保有以下配置：

```env
# IndexTTS2.5 配置
INDEXTTS_BASE_URL=http://localhost:8000
INDEXTTS_ENABLED=true
INDEXTTS_PATH=F:\IndexTTS2.5
INDEXTTS_TIMEOUT=60000
```

## 验证服务

启动服务后，可以通过以下方式验证：

1. **健康检查**：
   ```bash
   curl http://localhost:8000/api/health
   ```
   应该返回：
   ```json
   {
     "status": "ok",
     "message": "IndexTTS2.5 API Server",
     "available": true
   }
   ```

2. **获取音色列表**：
   ```bash
   curl http://localhost:8000/api/voices
   ```

3. **在浏览器中访问**：
   - API 服务器：http://localhost:8000
   - Web UI（如果使用原始启动）：http://localhost:7866

## 故障排除

### 问题：服务启动失败

1. **检查 Python 环境**：
   - 确保 `F:\IndexTTS2.5\python\python.exe` 存在
   - 或者确保系统 Python 已安装

2. **检查依赖**：
   - 确保所有依赖包已安装
   - 如果使用项目内置 Python，依赖应该已经安装

3. **检查端口占用**：
   ```bash
   netstat -ano | findstr :8000
   ```
   如果端口被占用，停止占用端口的进程或修改端口

### 问题：API 接口返回 404

- 确保使用的是 `api_server.py`，而不是 `webui.py`
- `webui.py` 是 Web UI，不提供 `/api/health` 等接口

### 问题：健康检查失败

- 检查服务是否正在运行
- 检查 `INDEXTTS_BASE_URL` 环境变量是否正确
- 查看服务日志，确认是否有错误信息

## 服务管理

### 启动服务
```bash
启动IndexTTS2.5-本地服务.bat
```

### 停止服务
- 在运行服务的命令行窗口中按 `Ctrl+C`
- 或者关闭命令行窗口

### 查看日志
服务启动后，日志会直接显示在命令行窗口中

## 注意事项

1. **端口冲突**：确保端口 8000 未被其他程序占用
2. **Python 环境**：建议使用项目内置的 Python 环境（`F:\IndexTTS2.5\python`）
3. **首次启动**：首次启动可能需要加载模型，需要一些时间
4. **GPU 支持**：如果有 GPU，服务会自动使用 GPU 加速

