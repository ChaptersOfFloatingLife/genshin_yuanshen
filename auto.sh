#!/bin/bash

set -e  # 如果某个命令失败，立即退出脚本

# 设置起始日期 (YYYY-MM-DD)
start_date="2025-02-10"
start_time="18:00"

# 获取resource目录下所有.json文件
resources=($(ls resource/*.json | sed 's/\.json$//'))

for resource in "${resources[@]}"; do
    character=$(basename $resource)
    resource_path="resource/${character}.json"
    image_path="resource/${character}.jpg"
    
    # 计算当前日期 (在 macOS 和 Linux 下可能有些不同)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        current_date=$(date -j -f "%Y-%m-%d" "$start_date" "+%Y-%m-%d")
    else
        # Linux
        current_date=$(date -d "$start_date" "+%Y-%m-%d")
    fi

    publish_datetime="$current_date $start_time"
    echo "处理角色: $character"
    echo "使用图片: $image_path"

    cp $image_path output/tmp_image.jpg
    python scripts/produce_with_gpt.py $resource_path
    python image/add_text.py
    python voice/clone.py
    python video/generate.py
    python xhs/publish.py "$publish_datetime"
done
