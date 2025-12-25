# 视频增强功能安装和配置指南

## 📋 功能概述

视频增强功能包括：
1. **超分辨率**：提升视频分辨率（1080P -> 4K）
   - Real-ESRGAN（默认）
   - Waifu2x
2. **帧率提升**：提升视频帧率（24fps -> 60fps）
   - RIFE（默认，快速）
   - FILM（适合大运动/高遮挡，较慢）

## 🔧 安装依赖

### 1. Python 依赖

```bash
# 基础依赖
pip install opencv-python pillow numpy

# Real-ESRGAN
pip install realesrgan
# 或使用命令行工具
# 下载：https://github.com/xinntao/Real-ESRGAN/releases

# Waifu2x
pip install waifu2x
# 或使用命令行工具
# 下载：https://github.com/nihui/waifu2x-ncnn-vulkan-python

# RIFE
pip install rife
# 或从源码安装
git clone https://github.com/megvii-research/ECCV2022-RIFE.git
cd ECCV2022-RIFE
pip install -r requirements.txt

# FILM
pip install film
# 或从源码安装
git clone https://github.com/google-research/frame-interpolation.git
cd frame-interpolation
pip install -r requirements.txt

# TensorFlow Lite（用于加速）
pip install tensorflow-lite

# FFmpeg Python 绑定
pip install ffmpeg-python
```

### 2. 系统依赖

#### FFmpeg
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# 下载：https://ffmpeg.org/download.html
```

#### CUDA（可选，用于 GPU 加速）
```bash
# 如果使用 GPU 加速，需要安装 CUDA
# 参考：https://developer.nvidia.com/cuda-downloads
```

### 3. 模型文件

#### Real-ESRGAN 模型
```bash
# 下载模型文件
mkdir -p weights
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -O weights/RealESRGAN_x4plus.pth
```

#### RIFE 模型
```bash
# RIFE 模型通常包含在包中
# 如果没有，从官方仓库下载
```

#### FILM 模型
```bash
# FILM 模型通常包含在包中
# 如果没有，从官方仓库下载
```

## ⚙️ 环境变量配置

在 `.env` 或 Render 环境变量中添加：

```bash
# 启用 TensorFlow Lite 加速
USE_TFLITE=true

# 视频处理临时目录（可选）
VIDEO_PROCESSING_TEMP_DIR=/tmp/video_processing
```

## 🚀 使用说明

### 前端使用

1. **提升分辨率**：
   - 在历史记录页面，鼠标悬停在视频上
   - 点击右下角的蓝色分辨率按钮
   - 选择 Real-ESRGAN 或 Waifu2x
   - 等待处理完成（通常需要几分钟）

2. **提升帧率**：
   - 在历史记录页面，鼠标悬停在视频上
   - 点击右下角的绿色帧率按钮
   - 选择 RIFE（快速）或 FILM（大运动）
   - 如果选择 FILM，会提示处理时间较长
   - 系统会自动检测大运动并切换到 FILM（如果启用）

### 后端 API

#### 提升分辨率
```bash
POST /api/v1/video/history/{generation_id}/enhance-resolution
Content-Type: application/json

{
  "method": "real_esrgan",  # 或 "waifu2x"
  "scale": 2  # 放大倍数（2 = 2倍，1080P -> 4K）
}
```

#### 提升帧率
```bash
POST /api/v1/video/history/{generation_id}/enhance-fps
Content-Type: application/json

{
  "target_fps": 60,
  "method": "rife",  # 或 "film"
  "auto_switch": true  # 是否自动检测大运动并切换
}
```

## 🔍 智能切换逻辑

### 大运动/高遮挡检测

系统会自动检测视频是否有大运动或高遮挡：
- 使用光流法或帧差法分析视频帧
- 如果检测到大运动（平均帧差 > 30），自动切换到 FILM
- FILM 更适合处理大运动场景

### 性能优化

1. **TensorFlow Lite 加速**：
   - 启用 `USE_TFLITE=true` 环境变量
   - 可以显著加速处理速度

2. **GPU 加速**：
   - 如果服务器有 GPU，模型会自动使用 GPU
   - 需要安装 CUDA 和对应的 GPU 驱动

3. **批处理**：
   - 视频处理是逐帧进行的
   - 可以根据服务器性能调整批处理大小

## ⚠️ 注意事项

1. **处理时间**：
   - 5秒视频的超分辨率：通常 2-5 分钟
   - 5秒视频的插帧：通常 1-3 分钟（RIFE）或 3-8 分钟（FILM）

2. **存储空间**：
   - 处理后的视频文件较大（4K 视频可能几百 MB）
   - 确保有足够的存储空间

3. **服务器资源**：
   - 视频处理需要大量 CPU/GPU 资源
   - 建议在性能较好的服务器上运行

4. **错误处理**：
   - 如果处理失败，会返回错误信息
   - 原始视频不会被修改

## 🐛 故障排除

### 问题 1: 模型文件未找到

**解决**：
- 检查模型文件是否下载到正确位置
- 确认模型文件路径配置正确

### 问题 2: CUDA 错误

**解决**：
- 检查 CUDA 是否正确安装
- 确认 GPU 驱动版本兼容
- 如果不需要 GPU，可以强制使用 CPU

### 问题 3: 内存不足

**解决**：
- 减少批处理大小
- 使用较低分辨率的视频
- 增加服务器内存

### 问题 4: 处理时间过长

**解决**：
- 启用 GPU 加速
- 启用 TensorFlow Lite
- 使用更快的模型（RIFE 而不是 FILM）

## 📝 更新日志

- 2025-12-25: 初始版本
  - 支持 Real-ESRGAN 和 Waifu2x 超分辨率
  - 支持 RIFE 和 FILM 插帧
  - 自动检测大运动并切换方法
  - TensorFlow Lite 加速支持

