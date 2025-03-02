import os
import json
from openai import OpenAI
import argparse
from dotenv import load_dotenv
from typing import Union
import re

class ChatWithGPT:
    def __init__(self):
        """初始化 ChatWithGPT 类。
        
        该构造函数从 .env 文件中获取 OpenAI API 密钥、基础 URL 和模型。
        如果缺少任一配置，将抛出 ValueError 异常。
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.api_base = os.getenv("OPENAI_API_BASE")
        self.model = os.getenv("OPENAI_MODEL")
        print(self.api_key, self.api_base, self.model)
        if not self.api_key or not self.api_base or not self.model:
            raise ValueError("需要提供 OpenAI API 密钥、基础 URL 和模型")

    def generate_content(
        self,
        prompt: str,
        system_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """生成文案内容"""
        try:
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.api_base
            )
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"生成内容时发生错误: {str(e)}")
            return ""

    def read_prompt_from_file(self, file_path: str, is_json: bool = False) -> Union[str, dict]:
        """从文件中读取内容
        
        Args:
            file_path: 文件路径
            is_json: 是否为 JSON 格式文件
        
        Returns:
            Union[str, dict]: 如果是 JSON 文件返回字典，否则返回字符串内容
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                if is_json:
                    data = json.load(file)
                    return data
                else:
                    return file.read().strip()
        except FileNotFoundError:
            print(f"错误：找不到文件 {file_path}")
            return ""
        except Exception as e:
            print(f"读取文件时发生错误：{str(e)}")
            return ""

    def save_content(self, file_path: str, gpt_response: str, user_data: dict):
        """保存合并后的内容到文件
        
        Args:
            file_path: 输出文件路径
            gpt_response: GPT 生成的回复
            user_data: 用户的 JSON 数据
        """
        print("gpt_response", gpt_response)
        try:
            # 使用正则表达式提取 {} 内的 JSON 内容
            json_match = re.search(r'{.*}', gpt_response, re.DOTALL)
            if not json_match:
                raise ValueError("未找到有效的 JSON 内容")
            
            json_str = json_match.group()
            response_data = json.loads(json_str)
            
            # 更新 user_data 中的内容
            user_data['content'] = response_data
            user_data.pop('user_prompt', None)
            
        except (json.JSONDecodeError, ValueError) as e:
            print(f"JSON 解析错误: {str(e)}")
            # 如果解析失败，保存原始响应
            user_data['content'] = gpt_response
        
        try:
            user_data['cover_image'] = "output/image.jpg"

            name = user_data['name']
            user_data['content_extra'] = f"""{name}的提醒服务，把喜欢的角色语音设为提醒，让{name}的声音陪伴你的每一天，简单几步就能设置，手机通用哦~，如果有需要定制的内容，可以私信我哦~，创作不易求个关注\n自定义闹钟设置教程：可以看主页的设置置顶合集\n如何获取语音？点赞+关注，评论你想要的角色，私信我需要的语音，会第一时间发送资源\n主页更多专属原神语音等你解锁\n欢迎来群里和大家一起创作！大家一起脑洞文案，一起讨论，一起分享"""
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(user_data, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存文件时发生错误：{str(e)}")

# 使用示例
if __name__ == "__main__":
    # 加载 .env 文件
    load_dotenv()
    
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='生成AI文案内容')
    parser.add_argument('user_data', type=str,
                        help='用户数据JSON文件路径')
    
    args = parser.parse_args()
    
    # 创建 ChatWithGPT 实例，从环境变量读取 API key
    chat = ChatWithGPT()
    
    # 读取 prompts
    system_prompt = chat.read_prompt_from_file('scripts/genshin_prompts/system.txt', is_json=False)
    print(args.user_data)
    user_data = chat.read_prompt_from_file(args.user_data, is_json=True)
    print("user_data", user_data)
    user_prompt = user_data.get('user_prompt', '')

    # 获取 GPT 回复
    response = chat.generate_content(
        prompt=user_prompt,
        system_prompt=system_prompt
    )
    
    # 保存合并后的内容
    print("保持到 output/script.json")
    chat.save_content('output/script.json', response, user_data)