"""
API配置加载和智能体工具模块

提供从JSON配置文件加载API配置的功能，以及基于OpenAI API格式的问答智能体类。

使用方法:
    from HandsOn.utilities.api_config import load_config, QAgent, get_response
    
    # 方式1: 使用get_response函数（推荐，与chapter_3.ipynb兼容）
    config = load_config()
    response = get_response(system_prompt="你是一个助手", user_prompt="你好")
    
    # 方式2: 使用QAgent类
    agent = QAgent(platform="openai", config=config)
    answer = agent.ask("你好")
"""

import json
import os
from pathlib import Path
from openai import OpenAI


def load_config(config_path=None):
    """
    从JSON文件加载API配置
    自动查找配置文件：优先查找 HandsOn/config.json
    
    Args:
        config_path: 配置文件路径，如果为None则自动查找
    
    Returns:
        dict: 包含所有API配置的字典，如果失败返回None
    """
    # 如果未指定路径，自动查找配置文件
    if config_path is None:
        # 获取当前文件的目录
        current_dir = Path(__file__).parent.parent
        hands_on_dir = current_dir
        
        # 可能的配置文件位置（按优先级排序）
        possible_paths = [
            "config.json",  # 当前目录（如果notebook在HandsOn目录运行）
            str(hands_on_dir / "config.json"),  # HandsOn目录下的config.json
            "HandsOn/config.json",  # HandsOn子目录
            "../HandsOn/config.json",  # 上级目录的HandsOn文件夹
            os.path.join(os.getcwd(), "HandsOn", "config.json"),  # 绝对路径
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                config_path = path
                break
        
        if config_path is None:
            print("❌ 错误: 找不到配置文件")
            print("   请确保在 HandsOn/ 目录下存在 config.json 文件")
            print("   可以从 HandsOn/config.json.example 复制并填写你的API密钥")
            return None
    
    try:
        # 转换为绝对路径并读取
        config_path = os.path.abspath(config_path)
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"✅ 成功加载配置文件: {config_path}")
        return config
    except FileNotFoundError:
        print(f"❌ 错误: 找不到配置文件 {config_path}")
        print("   请复制 HandsOn/config.json.example 为 HandsOn/config.json 并填写你的API密钥")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ 错误: JSON格式错误 - {e}")
        print(f"   请检查 {config_path} 文件的JSON语法")
        return None


class QAgent:
    """
    问答智能体类，支持从配置文件读取API信息
    兼容 OpenAI API 格式（OpenAI、ChatGLM等）
    """
    def __init__(self, api_key=None, base_url=None, model=None, 
                 platform="openai", config=None, 
                 system_prompt="你是一个很聪明的智能体。你会用中文回答用户提出的任何问题。"):
        """
        初始化智能体
        
        Args:
            api_key: API密钥（可选，优先使用直接提供的参数）
            base_url: API基础URL（可选，优先使用直接提供的参数）
            model: 模型名称（可选，优先使用直接提供的参数）
            platform: 平台名称，用于从config中读取配置（可选: "openai", "chatglm"）
            config: 配置字典（可选，如果不提供则自动从文件加载）
            system_prompt: 系统提示词，定义智能体角色和行为
        """
        # 如果提供了config参数，使用它；否则从文件加载
        if config is None:
            config = load_config()
        
        # 优先使用直接提供的参数，否则从config中读取
        if config:
            platform_config = config.get(platform, {})
            self.api_key = api_key or platform_config.get("api_key")
            self.base_url = base_url or platform_config.get("base_url")
            self.model = model or platform_config.get("model")
        else:
            # 如果没有config，必须提供参数
            if not all([api_key, base_url, model]):
                raise ValueError(
                    "❌ 错误: 配置文件不可用且未提供完整参数。\n"
                    "   请提供 api_key、base_url 和 model 参数，"
                    "   或创建 HandsOn/config.json 配置文件"
                )
            self.api_key = api_key
            self.base_url = base_url
            self.model = model
        
        # 验证必要参数
        if not self.api_key or not self.base_url or not self.model:
            raise ValueError(
                f"❌ 错误: 未找到 {platform} 的完整API配置。\n"
                f"   请检查 HandsOn/config.json 文件，确保包含以下字段：\n"
                f"   - api_key\n"
                f"   - base_url\n"
                f"   - model"
            )
        
        self.platform = platform
        self.system_prompt = system_prompt
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        
        print(f"✅ 智能体初始化成功")
        print(f"   平台: {platform.upper()}")
        print(f"   模型: {self.model}")
        print(f"   API地址: {self.base_url}")

    def ask(self, question, temperature=0.7, max_tokens=2048):
        """
        提问接口
        
        Args:
            question: 用户问题
            temperature: 温度参数（控制随机性，0-1之间）
            max_tokens: 最大生成token数
        
        Returns:
            str: 智能体的回答
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": question},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ 错误: {str(e)}"
    
    def update_system_prompt(self, system_prompt):
        """更新系统提示词"""
        self.system_prompt = system_prompt
        print("✅ 系统提示词已更新")


# 全局默认agent实例（用于get_response函数）
_default_agent = None


def get_response(system_prompt="", user_prompt="", model=None, temperature=0.0, top_p=1.0, 
                 max_tokens=2048, platform="openai", config=None, agent=None):
    """
    通用的API调用函数，用于提示工程实践
    参考 chapter_3.ipynb 中的实现
    
    Args:
        system_prompt: 系统提示词（可选）
        user_prompt: 用户提示词（必需）
        model: 模型名称（可选，如果不提供则使用配置中的默认模型）
        temperature: 温度参数（控制随机性，0-1之间，默认0.0）
        top_p: nucleus sampling参数（默认1.0）
        max_tokens: 最大生成token数（默认2048）
        platform: 平台名称，用于从config中读取配置（默认"openai"）
        config: 配置字典（可选，如果不提供则自动从文件加载）
        agent: QAgent实例（可选，如果提供则直接使用其client和配置）
    
    Returns:
        str: 模型的回答
    """
    global _default_agent
    
    if not user_prompt:
        return "❌ 错误: 用户提示词不能为空"
    
    # 如果提供了agent，使用其client和配置
    if agent is not None:
        client = agent.client
        use_model = model or agent.model
    else:
        # 如果没有默认agent，创建一个
        if _default_agent is None:
            if config is None:
                config = load_config()
            _default_agent = QAgent(platform=platform, config=config)
        client = _default_agent.client
        use_model = model or _default_agent.model
    
    # 使用传入的system_prompt（即使是空字符串也使用）
    # 参考chapter_3.ipynb的实现，直接使用传入的system_prompt
    use_system_prompt = system_prompt
    
    try:
        # 调用API（参考chapter_3.ipynb的实现）
        response = client.chat.completions.create(
            model=use_model,
            messages=[
                {"role": "system", "content": use_system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ 错误: {str(e)}"


def set_default_agent(agent):
    """
    设置默认的agent实例，供get_response函数使用
    
    Args:
        agent: QAgent实例
    """
    global _default_agent
    _default_agent = agent


# 如果直接运行此文件，进行测试
if __name__ == "__main__":
    # 加载配置
    config = load_config()
    
    # 查看已配置的API平台（不显示密钥）
    if config:
        print("\n📋 已配置的API平台:")
        for platform in config.keys():
            model_name = config[platform].get('model', 'N/A')
            base_url = config[platform].get('base_url', 'N/A')
            has_key = bool(config[platform].get('api_key'))
            status = "✅" if has_key else "⚠️"
            print(f"  {status} {platform.upper()}: {model_name} @ {base_url}")
