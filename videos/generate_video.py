from moviepy import ImageClip, AudioFileClip, CompositeVideoClip

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
    # 示例使用
    image_path = "/Users/xpw/ws/genshin_yuanshen/videos/resource/散兵_封面.jpg"    # 替换为你的图片路径
    audio_path = "/Users/xpw/ws/genshin_yuanshen/videos/resource/散兵_这是一条新的通知.wav"    # 替换为你的音频路径
    output_path = "/Users/xpw/ws/genshin_yuanshen/videos/output/output_video.mp4"         # 输出视频路径
    
    generate_video(image_path, audio_path, output_path)
