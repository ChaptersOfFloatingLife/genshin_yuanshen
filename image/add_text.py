from PIL import Image, ImageDraw, ImageFont
import os
import json

def calculate_font_size(text, font_path, target_width, initial_size=60):
    """
    计算合适的字体大小
    
    Args:
        text (str): 要绘制的文字
        font_path (str): 字体文件路径
        target_width (int): 目标宽度
        initial_size (int): 初始字体大小
    
    Returns:
        tuple: (font, actual_width, actual_height) 字体对象、实际宽度和高度
    """
    font_size_test = initial_size
    font = ImageFont.truetype(font_path, font_size_test)
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    
    # 动态调整字体大小
    while text_width < target_width and font_size_test < 200:
        font_size_test += 5
        font = ImageFont.truetype(font_path, font_size_test)
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
    
    while text_width > target_width and font_size_test > 20:
        font_size_test -= 5
        font = ImageFont.truetype(font_path, font_size_test)
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
    
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    return font, text_width, text_height

def add_artistic_text(image_path, text1, text2, output_path=None, 
                     font_path="fonts/SimHei.ttf", 
                     text_color=(255, 255, 255)):
    """
    给图片添加两行艺术文字
    
    Args:
        image_path (str): 输入图片路径
        text1 (str): 第一行文字
        text2 (str): 第二行文字
        output_path (str): 输出路径
        font_path (str): 字体文件路径
        text_color (tuple): 文字颜色
    """
    # 打开图片
    img = Image.open(image_path)
    
    # 调整图片大小为 600x800，保持宽高比
    target_size = (600, 800)
    img.thumbnail(target_size, Image.Resampling.LANCZOS)
    
    # 创建新的白色背景图片
    new_img = Image.new('RGB', target_size, (255, 255, 255))
    
    # 将调整后的图片粘贴到中心位置
    paste_x = (target_size[0] - img.width) // 2
    paste_y = (target_size[1] - img.height) // 2
    new_img.paste(img, (paste_x, paste_y))
    
    # 使用新的图片继续处理
    img = new_img
    
    # 创建可绘制对象
    draw = ImageDraw.Draw(img)
    
    # 加载字体
    try:
        # macOS 系统常见粗体字体路径
        font_path = "/System/Library/Fonts/Hiragino Sans GB.ttc"  # 冬青黑体
        if not os.path.exists(font_path):
            raise FileNotFoundError("未找到字体文件")
            
        print(f"使用字体: {font_path}")
    except Exception as e:
        print(f"警告: 加载字体失败 ({str(e)})，使用默认字体")
        font = ImageFont.load_default()
    
    # 文字样式设置（移到函数开头）
    text_color = (255, 255, 255)  # 白色
    outline_color = (0, 0, 0)     # 黑色
    outline_width = 3             # 描边宽度
    
    # 处理 text1，如果超过10个字则分两行
    if len(text1) > 10:
        # 尽量在中间位置分行
        mid_point = len(text1) // 2
        # 从中间向两边寻找适合的分割点（标点符号或空格）
        split_point = mid_point
        for i in range(min(5, mid_point)):  # 在中间位置前后5个字符内寻找
            if text1[mid_point-i] in '，。！？、 ,!?.':
                split_point = mid_point-i+1
                break
            if text1[mid_point+i] in '，。！？、 ,!?.':
                split_point = mid_point+i+1
                break
        
        text1_line1 = text1[:split_point]
        text1_line2 = text1[split_point:]
        
        # 计算第一行文字的字体大小和位置
        target_width1 = int(img.width * 0.8)
        font1, text_width1, text_height1 = calculate_font_size(text1_line1, font_path, target_width1)
        x1 = (img.width - text_width1) // 2
        y1 = 50  # 距离顶部50像素
        
        # 计算第二行文字的字体大小和位置（使用相同的字体大小）
        bbox = font1.getbbox(text1_line2)
        text_width1_2 = bbox[2] - bbox[0]
        text_height1_2 = bbox[3] - bbox[1]
        x1_2 = (img.width - text_width1_2) // 2
        y1_2 = y1 + text_height1 + 10  # 第一行文字下方10像素
        
        # 绘制text1第一行
        for offset_x in range(-outline_width, outline_width + 1):
            for offset_y in range(-outline_width, outline_width + 1):
                if offset_x == 0 and offset_y == 0:
                    continue
                draw.text(
                    (x1 + offset_x, y1 + offset_y),
                    text1_line1,
                    font=font1,
                    fill=outline_color
                )
        draw.text((x1, y1), text1_line1, font=font1, fill=text_color)
        
        # 绘制text1第二行
        for offset_x in range(-outline_width, outline_width + 1):
            for offset_y in range(-outline_width, outline_width + 1):
                if offset_x == 0 and offset_y == 0:
                    continue
                draw.text(
                    (x1_2 + offset_x, y1_2 + offset_y),
                    text1_line2,
                    font=font1,
                    fill=outline_color
                )
        draw.text((x1_2, y1_2), text1_line2, font=font1, fill=text_color)
        
    else:
        # 原来的单行text1处理逻辑
        target_width1 = int(img.width * 0.9)
        font1, text_width1, text_height1 = calculate_font_size(text1, font_path, target_width1)
        x1 = (img.width - text_width1) // 2
        y1 = 50  # 距离顶部50像素
        
        # 绘制单行text1
        for offset_x in range(-outline_width, outline_width + 1):
            for offset_y in range(-outline_width, outline_width + 1):
                if offset_x == 0 and offset_y == 0:
                    continue
                draw.text(
                    (x1 + offset_x, y1 + offset_y),
                    text1,
                    font=font1,
                    fill=outline_color
                )
        draw.text((x1, y1), text1, font=font1, fill=text_color)
    
    # 计算第二行文字的字体大小和位置（text2）
    target_width2 = int(img.width * 0.8)
    font2, text_width2, text_height2 = calculate_font_size(text2, font_path, target_width2)
    x2 = (img.width - text_width2) // 2
    y2 = img.height - text_height2 - 50  # 距离底部50像素
    
    # 绘制第二行文字
    for offset_x in range(-outline_width, outline_width + 1):
        for offset_y in range(-outline_width, outline_width + 1):
            if offset_x == 0 and offset_y == 0:
                continue
            draw.text(
                (x2 + offset_x, y2 + offset_y),
                text2,
                font=font2,
                fill=outline_color
            )
    draw.text((x2, y2), text2, font=font2, fill=text_color)
    
    # 保存图片
    os.makedirs("output", exist_ok=True)
    img.save("output/image.jpg")

if __name__ == "__main__":
    # 读取配置文件
    with open('output/script.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 从配置获取参数
    cover_image = "output/tmp_image.jpg"
    content = config['content']
    text1 = content['title']
    text2 = f"让全世界都听见 {config['name']}"
    
    # 处理图片
    add_artistic_text(cover_image, text1, text2)
    print("处理完成，图片已保存到 output/image.jpg")
    