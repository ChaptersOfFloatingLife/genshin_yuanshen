#!/bin/bash

set -e  # 如果某个命令失败，立即退出脚本

# 设置起始日期 (YYYY-MM-DD)
start_date="2025-01-20"
start_time="18:00"
resource_path="resource/wanye_万叶.json"
image_folder="resource/wanye_万叶"

echo "开始处理图片"
# 获取所有图片文件到数组
image_files=($(ls "$image_folder"/*.JPG 2>/dev/null))
echo "图片文件: ${image_files[@]}"
if [ ${#image_files[@]} -eq 0 ]; then
    echo "错误：在 $image_folder 中没有找到图片文件"
    exit 1
fi

echo "图片数量: ${#image_files[@]}"

# 遍历所有图片文件
for ((i=0; i<${#image_files[@]}; i++)); do
    current_image="${image_files[i]}"
    
    # 计算当前日期 (在 macOS 和 Linux 下可能有些不同)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        current_date=$(date -v+${i}d -j -f "%Y-%m-%d" "$start_date" "+%Y-%m-%d")
    else
        # Linux
        current_date=$(date -d "$start_date +$i days" "+%Y-%m-%d")
    fi
    
    publish_datetime="$current_date $start_time"
    echo "正在处理第 $((i+1))/${#image_files[@]} 张图片，发布时间: $publish_datetime"
    echo "使用图片: $current_image"
    cp $current_image output/tmp_image.jpg
    python scripts/produce_with_gpt.py $resource_path
    python image/add_text.py
    python voice/clone.py
    python video/generate.py
    python xhs/publish.py "$publish_datetime"
done
