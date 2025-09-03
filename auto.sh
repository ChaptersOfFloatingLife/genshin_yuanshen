#!/bin/bash

set -e  # 如果某个命令失败，立即退出脚本

# 激活 UV 虚拟环境
source .venv/bin/activate

# 设置起始日期为当前日期
start_date=$(date "+%Y-%m-%d")
start_time="18:00"
current_date=$start_date

# 获取resource目录下所有.json文件
resources=($(ls resource/*.json | sed 's/\.json$//'))

for resource in "${resources[@]}"; do
    character=$(basename $resource)
    resource_path="resource/${character}.json"
    image_path="resource/${character}.jpg"
    
    # 将当前日期加一天
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        current_date=$(date -j -v+1d -f "%Y-%m-%d" "$current_date" "+%Y-%m-%d")
    else
        # Linux
        current_date=$(date -d "$current_date +1 day" "+%Y-%m-%d")
    fi

    publish_datetime="$current_date $start_time"
    # echo "处理角色: $character"
    # echo "使用图片: $image_path"
    echo "发布时间: $publish_datetime"

    cp $image_path output/tmp_image.jpg
    python3 scripts/produce_with_gpt.py $resource_path
    python3 image/add_text.py
    python3 voice/clone.py
    python3 video/generate.py
    python3 xhs/publish.py "$publish_datetime"
done
