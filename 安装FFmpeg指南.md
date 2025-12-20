# Windows 安装 FFmpeg 指南

## 快速安装步骤

### 1. 下载 FFmpeg
访问：https://www.gyan.dev/ffmpeg/builds/

下载 **ffmpeg-release-essentials.zip**（推荐）或 **ffmpeg-release-full.zip**

### 2. 解压文件
解压到 `C:\ffmpeg\`（或其他你喜欢的路径）

### 3. 添加到环境变量
1. 按 `Win + X`，选择"系统"
2. 点击"高级系统设置"
3. 点击"环境变量"
4. 在"系统变量"中找到 `Path`，点击"编辑"
5. 点击"新建"，添加：`C:\ffmpeg\bin`（根据你的实际路径）
6. 点击"确定"保存

### 4. 验证安装
打开新的 PowerShell 或 CMD，运行：
```bash
ffmpeg -version
```

如果显示版本信息，说明安装成功！

### 5. 压缩视频
```bash
ffmpeg -i index.mp4 -c:v libx264 -crf 28 -preset slow -c:a aac -b:a 128k -movflags +faststart index-optimized.mp4
```

