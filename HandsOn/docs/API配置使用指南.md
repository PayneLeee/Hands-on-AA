# API 配置加载系统使用指南

## 📋 目录

- [设计理念](#设计理念)
- [快速开始](#快速开始)
- [配置文件格式](#配置文件格式)
- [核心组件](#核心组件)
- [使用方法](#使用方法)
- [安全注意事项](#安全注意事项)
- [常见问题](#常见问题)
- [扩展指南](#扩展指南)

---

## 设计理念

本 API 配置加载系统采用**统一配置、灵活使用**的设计理念，具有以下特点：

### 🎯 核心设计原则

1. **统一配置管理**
   - 所有 API 配置集中在 `config.json` 文件中
   - 支持多平台配置，便于切换和对比
   - 配置文件与代码分离，提高可维护性

2. **自动路径查找**
   - 智能查找配置文件位置，支持多种运行场景
   - 自动处理相对路径和绝对路径
   - 提供清晰的错误提示

3. **灵活的参数优先级**
   - 支持从配置文件读取（推荐）
   - 支持直接传参（用于临时覆盖）
   - 参数优先级：直接传参 > 配置文件 > 默认值

4. **安全性优先**
   - 配置文件自动加入 `.gitignore`，防止密钥泄露
   - 提供示例文件模板，方便团队协作
   - 清晰的错误提示，避免配置错误

5. **兼容性设计**
   - 兼容 OpenAI API 格式的所有平台
   - 统一的接口调用方式
   - 易于扩展新平台

---

## 快速开始

### 第一步：创建配置文件

1. 复制示例文件：
   ```bash
   cp HandsOn/config.json.example HandsOn/config.json
   ```

2. 编辑 `HandsOn/config.json`，填写你的 API 密钥：
   ```json
   {
     "openai": {
       "api_key": "sk-your-actual-api-key-here",
       "base_url": "https://api.openai.com/v1",
       "model": "gpt-4o-mini"
     }
   }
   ```

### 第二步：加载配置

```python
from pathlib import Path
import json
import os
from openai import OpenAI

# 加载配置（自动查找）
config = load_config()
```

### 第三步：创建智能体

```python
# 使用配置文件创建智能体
agent = QAgent(platform="openai", config=config)

# 提问
answer = agent.ask("什么是大模型智能体？")
print(answer)
```

---

## 配置文件格式

### 标准格式

`config.json` 采用 JSON 格式，结构如下：

```json
{
  "平台标识": {
    "api_key": "你的API密钥",
    "base_url": "API基础URL",
    "model": "模型名称"
  }
}
```

### 完整示例

```json
{
  "openai": {
    "api_key": "sk-proj-xxxxxxxxxxxxx",
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4o-mini"
  },
  "chatglm": {
    "api_key": "xxxxxxxxxxxxx.drd6kd",
    "base_url": "https://open.bigmodel.cn/api/coding/paas/v4",
    "model": "GLM-4.7"
  },
  "deepseek": {
    "api_key": "sk-xxxxxxxxxxxxx",
    "base_url": "https://api.deepseek.com",
    "model": "deepseek-chat"
  },
  "qwen": {
    "api_key": "sk-xxxxxxxxxxxxx",
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "model": "qwen-plus"
  }
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `api_key` | string | ✅ | API 密钥 | `"sk-proj-xxx..."` |
| `base_url` | string | ✅ | API 基础地址 | `"https://api.openai.com/v1"` |
| `model` | string | ✅ | 模型名称 | `"gpt-4o-mini"` |

### 支持的平台

| 平台标识 | 平台名称 | Base URL | 模型示例 |
|---------|---------|----------|---------|
| `openai` | OpenAI | `https://api.openai.com/v1` | `gpt-4o-mini`, `gpt-4`, `gpt-3.5-turbo` |
| `chatglm` | ChatGLM (智谱AI) | `https://open.bigmodel.cn/api/coding/paas/v4` | `GLM-4.7`, `chatglm-turbo` |
| `deepseek` | DeepSeek | `https://api.deepseek.com` | `deepseek-chat` |
| `qwen` | 通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-plus`, `qwen-turbo` |

> 💡 **提示**：只要平台支持 OpenAI 兼容的 API 接口格式，都可以使用相同的方式配置。

---

## 核心组件

### 1. `load_config()` 函数

**功能**：从 JSON 文件加载 API 配置，支持自动路径查找。

**函数签名**：
```python
def load_config(config_path=None):
    """
    从JSON文件加载API配置
    自动查找配置文件：优先查找 HandsOn/config.json
    
    Args:
        config_path: 配置文件路径，如果为None则自动查找
    
    Returns:
        dict: 包含所有API配置的字典，如果失败返回None
    """
```

**自动查找路径（按优先级）**：
1. `config.json` - 当前目录
2. `HandsOn/config.json` - HandsOn 子目录
3. `../HandsOn/config.json` - 上级目录的 HandsOn 文件夹
4. `os.path.join(os.getcwd(), "HandsOn", "config.json")` - 绝对路径

**使用示例**：
```python
# 方式1：自动查找（推荐）
config = load_config()

# 方式2：指定路径
config = load_config("HandsOn/config.json")
config = load_config("/absolute/path/to/config.json")
```

**返回值**：
- 成功：返回配置字典
- 失败：返回 `None`，并打印错误信息

### 2. `QAgent` 类

**功能**：问答智能体类，支持从配置文件读取 API 信息，兼容 OpenAI API 格式。

**初始化参数**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `api_key` | str | `None` | API 密钥（可选，优先使用） |
| `base_url` | str | `None` | API 基础 URL（可选，优先使用） |
| `model` | str | `None` | 模型名称（可选，优先使用） |
| `platform` | str | `"openai"` | 平台标识，用于从 config 读取 |
| `config` | dict | `None` | 配置字典（可选，不提供则自动加载） |
| `system_prompt` | str | `"你是一个很聪明的智能体..."` | 系统提示词 |

**参数优先级**：
1. 直接提供的参数（`api_key`, `base_url`, `model`）
2. 配置文件中的对应平台配置
3. 默认值或抛出错误

**主要方法**：

#### `ask(question, temperature=0.7, max_tokens=2048)`

提问接口，向智能体发送问题并获取回答。

**参数**：
- `question` (str): 用户问题
- `temperature` (float): 温度参数，控制随机性（0-1之间）
- `max_tokens` (int): 最大生成 token 数

**返回**：
- `str`: 智能体的回答，或错误信息

#### `update_system_prompt(system_prompt)`

更新系统提示词，改变智能体的角色和行为。

**参数**：
- `system_prompt` (str): 新的系统提示词

---

## 使用方法

### 基础用法

#### 方式1：使用配置文件（推荐）

```python
# 1. 加载配置
config = load_config()

# 2. 创建智能体
agent = QAgent(platform="openai", config=config)

# 3. 提问
answer = agent.ask("什么是大模型智能体？")
print(answer)
```

#### 方式2：直接指定参数

```python
# 直接提供所有参数（不推荐，密钥会暴露在代码中）
agent = QAgent(
    api_key="sk-your-api-key",
    base_url="https://api.openai.com/v1",
    model="gpt-4o-mini"
)
```

#### 方式3：混合使用（覆盖配置）

```python
# 从配置文件读取，但覆盖模型名称
config = load_config()
agent = QAgent(
    platform="openai",
    config=config,
    model="gpt-4"  # 覆盖配置文件中的模型
)
```

### 切换不同平台

```python
config = load_config()

# 使用 OpenAI
agent_openai = QAgent(platform="openai", config=config)
answer_openai = agent_openai.ask("你好")

# 使用 ChatGLM
agent_chatglm = QAgent(platform="chatglm", config=config)
answer_chatglm = agent_chatglm.ask("你好")

# 对比回答
print("OpenAI:", answer_openai)
print("ChatGLM:", answer_chatglm)
```

### 自定义系统提示词

```python
# 创建时指定
agent = QAgent(
    platform="openai",
    config=config,
    system_prompt="你是一个经验丰富的旅行家，擅长制定旅行攻略。"
)

# 或运行时更新
agent.update_system_prompt("你是一个专业的编程助手。")
answer = agent.ask("如何优化Python代码性能？")
```

### 调整生成参数

```python
# 使用较低温度，获得更确定性的回答
answer = agent.ask(
    "解释量子计算的基本原理",
    temperature=0.3,  # 降低随机性
    max_tokens=1000   # 限制长度
)

# 使用较高温度，获得更创造性的回答
creative_answer = agent.ask(
    "写一首关于春天的诗",
    temperature=0.9,  # 提高随机性
    max_tokens=500
)
```

### 错误处理

```python
# load_config() 会自动处理错误
config = load_config()
if config is None:
    print("配置加载失败，请检查配置文件")
    exit(1)

# QAgent 初始化会验证参数
try:
    agent = QAgent(platform="openai", config=config)
except ValueError as e:
    print(f"初始化失败: {e}")
    exit(1)

# ask() 方法会捕获 API 调用错误
answer = agent.ask("测试问题")
if answer.startswith("❌ 错误"):
    print(f"API 调用失败: {answer}")
```

---

## 安全注意事项

### ⚠️ 重要安全规则

1. **永远不要提交 `config.json` 到 Git**
   - ✅ 确保 `HandsOn/config.json` 在 `.gitignore` 中
   - ✅ 只提交 `config.json.example` 作为模板
   - ❌ 不要在代码中硬编码 API 密钥

2. **使用示例文件作为模板**
   ```bash
   # 首次使用时
   cp HandsOn/config.json.example HandsOn/config.json
   # 然后编辑 config.json，填写真实密钥
   ```

3. **定期轮换 API 密钥**
   - 如果密钥泄露，立即在平台后台撤销
   - 更新配置文件中的新密钥

4. **不要在公共场合分享配置文件**
   - 不要截图包含密钥的配置文件
   - 不要通过聊天工具发送配置文件

### 检查 `.gitignore`

确保 `.gitignore` 包含以下内容：

```gitignore
# API 配置文件
HandsOn/config.json
**/config.json
!HandsOn/config.json.example
```

### 验证配置未被跟踪

```bash
# 检查 Git 状态
git status

# 如果 config.json 出现在未跟踪文件中，说明 .gitignore 配置正确
# 如果出现在已跟踪文件中，需要从 Git 中移除：
git rm --cached HandsOn/config.json
```

---

## 常见问题

### Q1: 找不到配置文件

**错误信息**：
```
❌ 错误: 找不到配置文件
   请确保在 HandsOn/ 目录下存在 config.json 文件
```

**解决方案**：
1. 检查文件是否存在：`ls HandsOn/config.json`
2. 如果不存在，从示例文件复制：
   ```bash
   cp HandsOn/config.json.example HandsOn/config.json
   ```
3. 填写真实的 API 密钥

### Q2: JSON 格式错误

**错误信息**：
```
❌ 错误: JSON格式错误 - Expecting ',' delimiter: line 5 column 3
```

**解决方案**：
1. 检查 JSON 语法：
   - 确保所有字符串用双引号 `"` 包裹
   - 确保最后一个字段后没有逗号
   - 确保所有括号匹配
2. 使用在线 JSON 验证工具检查格式
3. 参考 `config.json.example` 的格式

### Q3: API 认证失败

**错误信息**：
```
❌ 错误: Incorrect API key provided
```

**可能原因**：
1. API 密钥错误或过期
2. 密钥格式不正确（缺少前缀或包含多余空格）
3. 平台配置错误（base_url 不正确）

**解决方案**：
1. 检查 `config.json` 中的 `api_key` 是否正确
2. 确认密钥在平台后台是否有效
3. 检查 `base_url` 是否与平台文档一致

### Q4: 模型不存在

**错误信息**：
```
❌ 错误: Model 'xxx' does not exist
```

**解决方案**：
1. 检查 `model` 字段的拼写
2. 参考平台文档确认正确的模型名称
3. 确认你的账户有权限使用该模型

### Q5: 连接超时

**错误信息**：
```
❌ 错误: Connection timeout
```

**可能原因**：
1. 网络连接问题
2. `base_url` 配置错误
3. 防火墙或代理设置

**解决方案**：
1. 检查网络连接
2. 验证 `base_url` 是否正确
3. 如果使用代理，配置环境变量或使用代理设置

### Q6: 如何添加新平台？

**步骤**：
1. 在 `config.json` 中添加新平台配置：
   ```json
   {
     "new_platform": {
       "api_key": "your-api-key",
       "base_url": "https://api.newplatform.com/v1",
       "model": "model-name"
     }
   }
   ```
2. 使用新平台：
   ```python
   agent = QAgent(platform="new_platform", config=config)
   ```

**要求**：
- 平台必须支持 OpenAI 兼容的 API 格式
- API 接口路径为 `/chat/completions`
- 请求格式与 OpenAI 一致

---

## 扩展指南

### 添加自定义配置字段

如果需要添加额外的配置字段（如超时时间、重试次数等），可以：

1. **扩展配置文件格式**：
   ```json
   {
     "openai": {
       "api_key": "sk-xxx",
       "base_url": "https://api.openai.com/v1",
       "model": "gpt-4o-mini",
       "timeout": 30,
       "max_retries": 3
     }
   }
   ```

2. **修改 `QAgent` 类读取新字段**：
   ```python
   class QAgent:
       def __init__(self, ...):
           # ... 现有代码 ...
           platform_config = config.get(platform, {})
           self.timeout = platform_config.get("timeout", 30)
           self.max_retries = platform_config.get("max_retries", 3)
   ```

### 支持环境变量

可以扩展 `load_config()` 函数，支持从环境变量读取配置：

```python
import os

def load_config(config_path=None, use_env=False):
    config = {}
    
    # 从环境变量读取（如果启用）
    if use_env:
        config["openai"] = {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        }
    
    # 从文件读取（如果存在）
    if config_path or os.path.exists("HandsOn/config.json"):
        file_config = load_config_from_file(config_path)
        # 合并配置，文件配置优先
        config.update(file_config)
    
    return config
```

### 添加配置验证

可以添加配置验证函数，确保配置的完整性：

```python
def validate_config(config):
    """验证配置文件的完整性和正确性"""
    required_fields = ["api_key", "base_url", "model"]
    errors = []
    
    for platform, platform_config in config.items():
        for field in required_fields:
            if field not in platform_config:
                errors.append(f"{platform}: 缺少字段 '{field}'")
            elif not platform_config[field]:
                errors.append(f"{platform}: 字段 '{field}' 为空")
    
    if errors:
        raise ValueError("配置验证失败:\n" + "\n".join(errors))
    
    return True

# 使用
config = load_config()
validate_config(config)
```

### 支持多环境配置

可以支持开发、测试、生产等多环境配置：

```json
{
  "development": {
    "openai": {
      "api_key": "dev-key",
      "base_url": "https://api.openai.com/v1",
      "model": "gpt-3.5-turbo"
    }
  },
  "production": {
    "openai": {
      "api_key": "prod-key",
      "base_url": "https://api.openai.com/v1",
      "model": "gpt-4"
    }
  }
}
```

```python
def load_config(config_path=None, environment="development"):
    config = load_config_from_file(config_path)
    return config.get(environment, {})
```

---

## 总结

本 API 配置加载系统提供了：

✅ **统一的配置管理** - 所有 API 配置集中管理  
✅ **灵活的使用方式** - 支持配置文件、直接传参、混合使用  
✅ **自动路径查找** - 智能查找配置文件位置  
✅ **完善的错误处理** - 清晰的错误提示和验证  
✅ **安全性保障** - 配置文件自动忽略，防止密钥泄露  
✅ **易于扩展** - 支持添加新平台和自定义字段  

通过遵循本指南，你可以安全、高效地管理多个 API 平台的配置，并在不同平台间灵活切换。

---

## 相关文件

- `HandsOn/config.json.example` - 配置文件模板
- `HandsOn/Lecture1Notes.ipynb` - 完整使用示例
- `.gitignore` - Git 忽略规则

---

**最后更新**：2025年1月
