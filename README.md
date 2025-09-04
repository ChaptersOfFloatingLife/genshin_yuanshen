# 原神角色 AI 语音克隆 & 小红书文案生成器 🎭

一个有趣的项目，让你的原神角色说出你想说的话，还能自动生成小红书风格的文案！

## ✨ 特色功能

- 🎤 **原神角色语音克隆**：让魈、派蒙、胡桃等角色为你发声
- 📝 **小红书风格文案生成**：自动生成吸睛的小红书文案
- 🚀 **HTTP API 发布**：通过 HTTP 接口快速发布内容到小红书
- 🎥 **自动视频下载**：支持从 URL 自动下载视频并发布
- 🤖 **AI 驱动**：基于最新的 AI 技术，包括 GPT 和语音克隆模型
- 🎯 **简单易用**：友好的命令行界面和 REST API，轻松上手

## 🚀 快速开始

### 前置要求
- Python 3.9+
- [UV](https://docs.astral.sh/uv/) 包管理器

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd genshin_yuanshen
```

2. **安装依赖**
```bash
# 使用 UV 安装所有依赖
uv sync
```

3. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，添加你的 API 密钥
```

4. **运行项目**
```bash
# 自动运行所有角色
bash auto.sh

# 或者单独运行某个步骤
uv run python scripts/produce_with_gpt.py resource/Xiao_魈.json
```

### 手动步骤运行

如果你想分步骤运行，可以使用以下命令：

```bash
# 激活环境
source .venv/bin/activate

# 生成脚本/剧本
python3 scripts/produce_with_gpt.py resource/Xiao_魈.json

# 添加文字
python3 image/add_text.py

# 克隆语音
python3 voice/clone.py

# 合成视频
python3 video/generate.py

# 生成小红书 cookie（需要手动登录，暂未找到官方 API），仅需执行一次
python3 xhs/fetch_cookies.py

# 发布小红书
python3 xhs/publish.py "2025-01-12 16:00"
```

## 🌐 HTTP API 发布

新增的 HTTP API 让发布内容变得更简单！

### 启动 API 服务器

```bash
# 启动 API 服务器
python xhs/api_server.py

# 服务器将在 http://localhost:8000 启动
# API 文档: http://localhost:8000/docs
```

### API 使用方法

**发布内容到小红书**（支持视频 URL 自动下载）:

```bash
  curl -X POST "http://localhost:8000/publish" \
    -H "Content-Type: application/json" \
    -d '{
      "name": "魈",
      "tags": "#原神 #魈 #声控",
      "content": {
        "title": "魈的测试",
        "script": "测试API功能"
      },
      "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
      "publish_time": "2026-01-01 18:00"
    }'
```

## 🛠️ 技术栈

- OpenAI GPT API
- TTS 语音克隆模型
- Python 3.8+

## 🎮 适用场景

- 原神同人创作
- 视频配音
- 社交媒体内容创作
- AI 技术学习与实验

## 📝 注意事项

- 请遵守相关平台的使用条款
- 仅供学习和个人使用
- 需要 API 密钥才能使用完整功能

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！让我们一起完善这个项目。

## 📄 许可证

MIT License

## ⭐ 支持项目

如果这个项目对你有帮助，欢迎给个 Star！

## 📧 联系方式

- GitHub Issues
- Email: wuxiangping0313@gmail.com

---

**免责声明**：本项目仅供学习和技术研究使用。请勿用于商业用途或违反相关政策的行为。
