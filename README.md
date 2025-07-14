# AI-Content-Generator
AI多功能内容生成器 README.md
=================================

🌐 **一站式AI创作平台，让创意无限可能！**

本项目是一个基于 **Streamlit + LangChain + OpenAI API** 开发的 **AI多功能内容生成器**，集成了 **视频脚本生成、小红书文案创作、智能对话、PDF问答** 四大核心功能，提供美观易用的 Web 界面，帮助用户高效创作内容。

---

🚀 功能特色
----------

| 功能模块 | 描述 | 特点 |
|---|---|---|
| 🎬 **视频脚本生成器** | 根据主题、时长、创造力参数自动生成视频脚本 | 支持导出 Excel |
| 📱 **小红书文案生成器** | 根据主题和风格自动生成爆款小红书文案 | 自动配图 |
| 💬 **克隆GPT对话** | 支持连续对话、上下文记忆、对话导出 | 参数可调 |
| 📄 **PDF问答工具** | 上传PDF后，根据内容回答用户问题 | 支持多种回答风格 |

---
🖥️ 界面预览
----------


---
🛠️ 技术栈
----------

- **前端**：Streamlit
- **AI模型**：OpenAI GPT-3.5-turbo / text-embedding-3-large
- **框架**：LangChain
- **向量数据库**：FAISS
- **Python库**：
  - `streamlit`
  - `langchain`
  - `openai`
  - `pydantic`
  - `pandas`
  - `requests`

---

📦 项目结构
------------

```
AI-Content-Generator/
├── main.py                 # 主程序（Streamlit入口）
├── get_image.py            # 百度图片爬虫
├── utils1.py               # 视频脚本生成工具
├── utils2.py               # 小红书文案生成工具
├── utils3.py               # GPT对话工具
├── utils4.py               # PDF问答工具
├── xiaohongshu_model.py    # Pydantic数据模型
├── prompt_template.py      # Prompt模板
├── requirements.txt        # 依赖列表
└── README.md               # 项目说明
```

---

⚙️ 快速开始
------------

### 1. 克隆仓库

```bash
git clone https://github.com/Aygn-kkaho/AI-Content-Generator.git
cd AI-Content-Generator
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

在项目根目录创建 `.env` 文件：

```env
OPENAI_API_KEY=你的OpenAI API密钥
```

或直接修改 `utils*.py` 中的 `openai_api_key` 参数。

### 4. 运行项目

```bash
streamlit run main.py
```

🔑 API密钥获取
--------------

- **OpenAI官方**：[https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **代理服务**：[https://openai-hk.com/v3/ai/key](https://openai-hk.com/v3/ai/key)

---

📌 使用说明
------------

### 🎬 视频脚本生成器

1. 输入视频主题（如："如何提高工作效率"）
2. 设置视频时长（0.5-60分钟）
3. 调整创造力参数（0.0-1.0）
4. 点击生成，支持导出Excel

### 📱 小红书文案生成器

1. 输入文案主题（如："护肤心得"）
2. 选择写作风格（幽默/文艺/专业/严肃）
3. 自动生成标题+正文+推荐配图

### 💬 克隆GPT对话

1. 输入OpenAI API密钥
2. 开始连续对话
3. 支持导出对话记录为JSON

### 📄 PDF问答工具

1. 上传PDF文件（≤100MB）
2. 输入问题（如："总结文档要点"）
3. 选择回答风格（正式/非正式/技术/简洁/解释）
4. 获取基于PDF内容的精准回答

---

🙏 致谢
-------

- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [OpenAI](https://openai.com/)
- [FAISS](https://github.com/facebookresearch/faiss)

---


- **作者**：Aygn-kkaho
- **邮箱**：1391018262@qq.com
- **GitHub**：[https://github.com/Aygn-kkaho](https://github.com/Aygn-kkaho)

---

⭐ 如果本项目对你有帮助，请给个 Star！
