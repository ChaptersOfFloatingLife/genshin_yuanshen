import sys
import requests
import json
import os
from typing import Optional
import locale
from dotenv import load_dotenv

# 设置本地化编码
locale.getpreferredencoding = lambda: 'UTF-8'

# 设置命令行输出编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')  # Python 3.7+

class VoiceCloner:
    def __init__(self):
        """初始化 VoiceCloner 类。
        
        从 .env 文件中获取 API access token 和 URL。
        如果缺少配置，将抛出 ValueError 异常。
        """
        # 加载 .env 文件
        load_dotenv()
        
        self.access_token = os.getenv("VOICE_API_TOKEN")
        self.api_url = os.getenv("VOICE_API_URL")
        
        if not self.access_token or not self.api_url:
            raise ValueError("需要在 .env 文件中提供 VOICE_API_TOKEN 和 VOICE_API_URL")
        
    def clone_voice(
        self,
        text: str,
        speaker: str = "魈【原神】",
        emotion: str = "中立",
        text_language: str = "中文",
        speed_factor: float = 1.0,
        output_path: Optional[str] = None
    ) -> str:
        """克隆语音
        
        Args:
            text: 要合成的文本
            speaker: 说话人角色
            emotion: 情感类型
            text_language: 文本语言
            speed_factor: 语速
            output_path: 输出音频文件路径
            
        Returns:
            str: 音频文件路径
        """
        # 构建请求参数
        payload = {
            "access_token": self.access_token,
            "type": "tts",
            "brand": "gpt-sovits",
            "name": "anime",
            "method": "api",
            "prarm": {
                "speaker": speaker,
                "emotion": emotion,
                "text": text,
                "text_language": text_language,
                "text_split_method": "按标点符号切",
                "fragment_interval": 0.3,
                "batch_size": 1,
                "batch_threshold": 0.75,
                "parallel_infer": True,
                "split_bucket": True,
                "top_k": 10,
                "top_p": 1.0,
                "temperature": 1.0,
                "speed_factor": speed_factor
            }
        }

        try:
            # 添加中文调试信息
            print(f"正在请求API: {self.api_url}")
            print(f"请求参数: {json.dumps(payload, ensure_ascii=False, indent=2)}")
            
            response = requests.post(
                self.api_url,
                json=payload,
                headers={"content-type": "application/json"}
            )
            
            # Mac系统下的处理方式
            try:
                response_text = response.json()
                if isinstance(response_text, dict):
                    response_text = json.dumps(response_text, ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                response_text = response.text
            
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response_text}")
            
            if response.status_code != 200:
                error_msg = response_text
                print(f"错误信息: {error_msg}")
                raise Exception(error_msg)
                
            response.raise_for_status()
            
            result = response.json()
            
            if not result.get("audio"):
                raise Exception(f"语音合成失败: {result.get('message')}")
                
            # 下载音频文件
            audio_url = result["audio"]
            if output_path:
                audio_response = requests.get(audio_url)
                audio_response.raise_for_status()
                
                with open(output_path, "wb") as f:
                    f.write(audio_response.content)
                return output_path
            
            return audio_url
            
        except Exception as e:
            print(f"语音克隆失败: {str(e)}")
            raise

if __name__ == "__main__":
    # 示例使用
    cloner = VoiceCloner()
    
    # 从JSON文件读取生成的内容
    with open("output/script.json", "r", encoding="utf-8") as f:
        content = json.load(f)

    speaker = content["name"]
    text = content["content"]
    output_path = "output/voice.wav"
        
    # 克隆语音
    audio_path = cloner.clone_voice(
        text=text,
        speaker=speaker,
        output_path=output_path
    )
    
    print(f"语音文件已保存至: {audio_path}")
