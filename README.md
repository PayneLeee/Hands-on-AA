# Hands-on-AI: 动手学大模型智能体

欢迎来到《动手学大模型智能体》项目！这是一个系统性的实践教程，帮助您从零开始掌握大模型智能体的核心原理与实践方法。

## 📚 项目简介

本项目是一本关于大模型智能体的实践教材，涵盖了从基础概念到高级应用的完整内容。您将学习如何构建、调试和部署真正能"感知—思考—执行"的智能代理。

### 主要内容

- **Part 1: 基础篇** - 智能体基础概念、大语言模型原理、提示工程、评估与调试
- **Part 2: 架构篇** - 智能体架构概览、记忆管理、工具调用、推理与规划
- **Part 3: 微调篇** - 指令微调、LoRA、量化等模型优化技术
- **Part 4: 进阶篇** - 多模态智能体、Agent Protocols、安全与对抗

## 🚀 快速开始

### 环境要求

- Python 3.10 或更高版本
- CUDA 11.8+ (如果使用GPU)
- 8GB+ RAM (推荐16GB+)
- 足够的磁盘空间用于模型下载

### 安装步骤

#### 方法1: 使用 Conda (推荐)

1. **创建并激活conda环境**

```bash
# 创建conda环境
conda create -n hands-on-aai python=3.10 -y

# 激活环境
conda activate hands-on-aai
```

**注意**: 建议使用 `hands-on-aai` 作为环境名称。如果需要在终端中手动激活，可以运行：

```powershell
# PowerShell (Windows)
.\activate_env.ps1

# 或使用批处理文件 (Windows)
activate_env.bat

# 或直接使用conda命令 (所有平台)
conda activate hands-on-aai
```

2. **安装PyTorch (根据您的CUDA版本选择)**

```bash
# CPU版本
pip install torch torchvision torchaudio

# CUDA 11.8版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

3. **安装其他依赖**

```bash
pip install -r requirements.txt
```

#### 方法2: 使用 venv

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 验证安装

运行以下命令验证主要依赖是否安装成功：

```python
import torch
import transformers
import langchain
import openai

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Transformers version: {transformers.__version__}")
print(f"LangChain version: {langchain.__version__}")
```

## 📖 使用说明

### 运行Jupyter Notebook

1. **启动Jupyter Notebook**

```bash
jupyter notebook
```

2. **打开对应的章节文件**

按照章节顺序打开notebook文件：
- `part_1/chapter_1.ipynb` - 初探大模型智能体
- `part_1/chapter_2.ipynb` - 生成式大语言模型
- `part_1/chapter_3.ipynb` - 提示工程
- `part_1/chapter_4.ipynb` - 智能体评估与调试
- 等等...

### API密钥配置

部分章节需要使用API密钥（如DeepSeek、OpenAI等）。本项目支持两种配置方式：

**方式1: 使用配置文件（推荐）**

创建 `HandsOn/config.json` 文件（可参考 `HandsOn/config.json.example`）：

```json
{
  "openai": {
    "api_key": "your_api_key_here",
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4o-mini"
  }
}
```

详细配置方法请参考 `HandsOn/docs/API配置使用指南.md`。

**方式2: 使用环境变量**

创建 `.env` 文件并添加：

```env
# DeepSeek API (示例)
DEEPSEEK_API_KEY=your_api_key_here

# OpenAI API (可选)
OPENAI_API_KEY=your_api_key_here

# SerpAPI (用于搜索功能)
SERPAPI_API_KEY=your_api_key_here
```

然后在代码中使用：

```python
from dotenv import load_dotenv
load_dotenv()
```

## 📁 项目结构

```
Hands-on-aai/
├── part_1/              # 基础篇
│   ├── chapter_1.ipynb  # 初探大模型智能体
│   ├── chapter_2.ipynb  # 生成式大语言模型
│   ├── chapter_3.ipynb  # 提示工程
│   └── chapter_4.ipynb  # 智能体评估与调试
├── part_2/              # 架构篇
│   ├── chapter_5.ipynb  # 智能体架构概览
│   ├── chapter_6.ipynb  # 记忆管理与检索增强
│   ├── chapter_7.ipynb  # 外部工具调用
│   └── chapter_8.ipynb  # 推理、规划和树搜索增强
├── part_3/              # 微调篇
│   ├── chapter_9.ipynb  # 指令微调
│   ├── chapter_10.ipynb # LoRA与参数高效微调
│   └── chapter_11.ipynb # 量化
├── part_4/              # 进阶篇
│   ├── Chapter_12.ipynb # 多模态智能体
│   ├── chapter_13.ipynb # Agent Protocols
│   ├── chapter_14.ipynb # 智能体安全与对抗
│   └── Chapter_15.ipynb # MCP应用实践
├── requirements.txt     # Python依赖列表
└── README.md           # 本文件
```

## 🛠️ 主要技术栈

- **深度学习框架**: PyTorch
- **大语言模型**: Transformers (Hugging Face)
- **智能体框架**: LangChain, LangGraph
- **向量数据库**: FAISS
- **模型评估**: lm-eval, human-eval
- **开发环境**: Jupyter Notebook

## 📝 学习路径建议

1. **初学者路径**
   - 从 Part 1 开始，系统学习基础概念
   - 完成每个章节的实践代码
   - 尝试修改和扩展示例代码

2. **进阶路径**
   - 深入学习 Part 2 的架构设计
   - 实践 Part 3 的模型微调技术
   - 探索 Part 4 的高级应用

3. **实践项目**
   - 结合所学知识，构建自己的智能体应用
   - 参与开源项目贡献
   - 分享学习心得和经验

## ⚙️ 环境配置

### 完整配置指南

详细的环境配置说明请参考：

- **[环境配置完整指南](HandsOn/docs/环境配置完整指南.md)** - 完整的环境配置步骤（推荐新用户阅读）
- [API配置使用指南](HandsOn/docs/API配置使用指南.md) - 详细的API配置系统说明（包含设计理念、核心组件、使用方法等）

### IDE配置（可选）

如果您使用 Cursor 或 VS Code，可以配置IDE自动使用正确的Python解释器。详细配置方法请参考 [环境配置完整指南](HandsOn/docs/环境配置完整指南.md#ide配置)。

### 验证环境配置

运行以下命令验证环境是否正确配置：

```python
import sys
import torch
print(f"Python路径: {sys.executable}")
print(f"PyTorch版本: {torch.__version__}")
print(f"CUDA可用: {torch.cuda.is_available()}")
```

### 激活环境

根据您使用的平台和工具：

**使用 Conda:**
```bash
conda activate hands-on-aai
```

**使用 venv:**
```bash
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

**使用项目提供的脚本（Windows）:**
```powershell
# PowerShell
.\activate_env.ps1

# CMD
activate_env.bat
```

> **注意**: 如果使用项目提供的激活脚本，请先根据您的conda安装路径修改脚本中的路径。详见 [环境配置完整指南](HandsOn/docs/环境配置完整指南.md#ide配置)。

## 🔧 常见问题

### Q: 如何选择PyTorch版本？

A: 根据您的CUDA版本选择对应的PyTorch安装命令。如果没有GPU，使用CPU版本即可。

### Q: 模型下载失败怎么办？

A: 可以使用Hugging Face镜像站点，或在代码中设置镜像：

```python
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
```

### Q: 内存不足怎么办？

A: 可以使用量化模型、减小batch size，或使用CPU版本的模型。

### Q: API调用失败？

A: 请检查：
1. API密钥是否正确配置
2. 网络连接是否正常
3. API额度是否充足

## 🤝 贡献指南

欢迎提交Issue和Pull Request！如果您发现错误或有改进建议，请随时联系我们。

## 📄 许可证

本项目采用开源许可证，具体请查看LICENSE文件。

## 🙏 致谢

感谢所有为本项目做出贡献的开发者们！

## 📮 联系方式

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至项目维护者

---

**祝您学习愉快！** 🎉
