# 原神角色 AI 语音克隆 & 小红书文案生成器 🎭

一个有趣的项目，让你的原神角色说出你想说的话，还能自动生成小红书风格的文案！

## ✨ 特色功能

- 🎤 **原神角色语音克隆**：让魈、派蒙、胡桃等角色为你发声
- 📝 **小红书风格文案生成**：自动生成吸睛的小红书文案
- 🤖 **AI 驱动**：基于最新的 AI 技术，包括 GPT 和语音克隆模型
- 🎯 **简单易用**：友好的命令行界面，轻松上手

## 🚀 快速开始

1. 克隆项目
2. 安装依赖
3. 运行

```
# For auto run
bash auto.sh
```

# 生成脚本/剧本
```
# 生成脚本/剧本
python scripts/produce_with_gpt.py resource/Xiao_魈.json

# 添加文字
python image/add_text.py

# 克隆语音
python voice/clone.py

# 合成视频
python video/generate.py

# 生成小红书 cookie（需要手动登录，暂未找到官方 API），仅需执行一次
python xhs/fetch_cookies.py

> 请在浏览器中完成登录，然后按回车继续...
> 已保存 13 个 cookies

# 发布小红书
python xhs/publish.py "2025-01-12 16:00"
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
