from moviepy import ImageClip, AudioFileClip, CompositeVideoClip
import json

def generate_video(image_path, audio_path, output_path):
    """
    将图片和音频合成为视频
    
    参数:
        image_path: 图片文件路径
        audio_path: 音频文件路径
        output_path: 输出视频文件路径
    """
    # 加载音频文件
    audio = AudioFileClip(audio_path)
    
    # 创建图片剪辑，持续时间与音频相同
    image = ImageClip(image_path).with_duration(audio.duration)
    
    # 将音频添加到图片中
    video = image.with_audio(audio)
    
    # 生成视频文件
    video.write_videofile(output_path, fps=24)
    
    # 清理资源
    audio.close()
    video.close()

if __name__ == "__main__":
    # 读取脚本配置
    with open("output/script.json", "r", encoding="utf-8") as f:
        script = json.load(f)
    
    image_path = script["cover_image"]    # 从script.json中读取封面图片路径
    audio_path = "output/voice.wav"    # 替换为你的音频路径
    output_path = "output/video.mp4"         # 输出视频路径
    
    generate_video(image_path, audio_path, output_path)
