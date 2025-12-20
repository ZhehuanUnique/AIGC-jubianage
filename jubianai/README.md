# 视频生成 Playground

基于 Streamlit + FastAPI 的视频生成应用，支持接入 Seedance 1.0 Fast 模型。

## 功能特性

- 🎬 视频生成：从文本提示词生成高质量视频
- 🎨 灵活配置：可调整视频尺寸、时长、帧率等参数
- 📚 历史记录：查看之前的生成结果
- 🔐 API Key 管理：安全的 API Key 配置
- 🚀 现代化界面：美观易用的 Streamlit 界面

## 项目结构

```
jubianai/
├── frontend/
│   └── app.py              # Streamlit 前端应用
├── backend/
│   └── api.py              # FastAPI 后端服务
├── config.py               # 配置文件
├── requirements.txt        # Python 依赖
├── start_backend.bat       # Windows 后端启动脚本
├── start_frontend.bat      # Windows 前端启动脚本
├── start_backend.sh        # Linux/Mac 后端启动脚本
├── start_frontend.sh       # Linux/Mac 前端启动脚本
└── README.md              # 项目文档
```

## 安装步骤

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量（可选）

创建 `.env` 文件并填入您的配置：

```env
API_KEY=your_api_key_here
SEEDANCE_API_ENDPOINT=https://api.example.com/v1/video/generate
HOST=0.0.0.0
PORT=8000
```

**注意**：也可以在 Streamlit 前端界面的侧边栏直接输入 API Key，无需配置文件。

### 3. 启动后端服务

```bash
python backend/api.py
```

或者使用 uvicorn：

```bash
uvicorn backend.api:app --host 0.0.0.0 --port 8000 --reload
```

### 4. 启动前端界面

```bash
streamlit run frontend/app.py
```

前端界面将在浏览器中自动打开（默认地址：http://localhost:8501）

## 使用说明

1. 在侧边栏输入您的 API Key
2. 在主界面输入视频描述（提示词）
3. （可选）调整高级参数，如尺寸、时长、帧率等
4. 点击"生成视频"按钮
5. 等待视频生成完成

## 接入 Seedance 1.0 Fast

目前后端 API 已经预留了 Seedance 1.0 Fast 的接入接口。您需要：

1. 在 `backend/api.py` 的 `generate_video` 函数中实现实际的 API 调用
2. 根据 Seedance API 文档调整请求格式和参数
3. 实现视频状态查询功能（`get_video_status`）

示例代码已包含在 `backend/api.py` 中，取消注释并修改相应部分即可。

## 架构说明

### 前端
- **Streamlit**：用于快速构建用户界面
  - 优点：开发快速，适合原型和内部工具
  - 缺点：自定义样式有限，复杂交互支持较弱

### 后端
- **FastAPI**：现代、高性能的 Python Web 框架
  - 支持异步处理
  - 自动生成 API 文档
  - 类型检查和验证

### 关于 Streamlit vs 传统前端框架

**Streamlit**：
- 适合快速原型、数据应用、内部工具
- 适合对话式界面和简单的表单交互
- 开发速度快，但自定义能力有限

**传统前端框架（React/Vue + FastAPI）**：
- 适合复杂的用户交互
- 更好的自定义样式和动画
- 更适合面向最终用户的产品

本项目使用 Streamlit 作为起点，后续可以根据需求升级到 React/Vue 等框架。

## 关于 Agent 和 ComfyUI

### Agent 方式
- 适合复杂的任务编排和多步骤处理
- 可以处理视频生成的多个阶段（预处理、生成、后处理等）
- 需要编写更多的业务逻辑代码

### ComfyUI 工作流
- 基于节点的可视化工作流
- 适合图像/视频生成任务
- 可以通过 API 调用 ComfyUI 工作流

建议：
- 如果 Seedance 1.0 Fast 提供直接的 API 接口，使用 FastAPI 直接调用即可
- 如果需要复杂的工作流，可以考虑 ComfyUI
- 如果需要智能任务调度和错误处理，可以使用 Agent 框架

## 开发计划

- [x] 基础前端界面（Streamlit）
- [x] 后端 API 框架（FastAPI）
- [ ] 接入 Seedance 1.0 Fast API
- [ ] 视频状态轮询和实时更新
- [ ] 视频预览和下载功能
- [ ] 错误处理和重试机制
- [ ] （可选）升级到 React/Vue 前端

## 许可证

MIT License

