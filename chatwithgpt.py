import openai
import os
from typing import Optional, List, Dict, Any

class ChatWithGPT:
    def __init__(self, api_key: Optional[str] = None):
        """初始化 ChatWithGPT 类
        
        Args:
            api_key: OpenAI API key。如果不提供，将从环境变量获取
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("需要提供 OpenAI API key")
        
        openai.api_key = self.api_key
        openai.api_base = "https://api.chatanywhere.tech/v1"

    def generate_content(
        self,
        prompt: str,
        system_prompt: str,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """生成文案内容
        
        Args:
            prompt: 用户输入的提示词
            system_prompt: 系统提示词/开发者提示词
            model: 使用的模型，默认为 gpt-3.5-turbo
            temperature: 温度参数，控制输出的随机性，默认为 0.7
            max_tokens: 最大生成的 token 数量，默认为 1000
            
        Returns:
            生成的文案内容
        """
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"生成内容时发生错误: {str(e)}")
            return ""

    def read_prompt_from_file(self, file_path: str) -> str:
        """从文件中读取 prompt"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except FileNotFoundError:
            print(f"错误：找不到文件 {file_path}")
            return ""
        except Exception as e:
            print(f"读取文件时发生错误：{str(e)}")
            return ""

# 使用示例
if __name__ == "__main__":
    # 创建 ChatWithGPT 实例
    chat = ChatWithGPT(api_key="")
    
    # 读取 prompt
    system_prompt = chat.read_prompt_from_file('prompts/system_prompt.txt')
    user_prompt = chat.read_prompt_from_file('prompts/user_prompt.txt')

    # 确保 prompt 不为空
    if not system_prompt or not user_prompt:
        print("错误：无法读取 prompt 文件")
        exit(1)

    # 生成内容
    response = chat.generate_content(
        prompt=user_prompt,
        system_prompt=system_prompt
    )
    
    # 将生成的内容写入 txt 文件
    with open("generated_content.txt", "w", encoding="utf-8") as file:
        file.write(response)
    
    print("生成的内容已保存到 generated_content.txt 文件中")
