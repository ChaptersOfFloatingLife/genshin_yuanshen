#!/bin/bash

set -e  # 如果某个命令失败，立即退出脚本

# 设置起始日期 (YYYY-MM-DD)
start_date="2025-01-17"
start_time="20:00"
resource_path="resource/Scaramouche_散兵.json"

# 循环7次
for i in {1..7}; do
    # 计算当前日期 (在 macOS 和 Linux 下可能有些不同)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        current_date=$(date -v+${i}d -j -f "%Y-%m-%d" "$start_date" "+%Y-%m-%d")
    else
        # Linux
        current_date=$(date -d "$start_date +$i days" "+%Y-%m-%d")
    fi
    
    publish_datetime="$current_date $start_time"
    echo "正在安排第 $((i)) 次发布，发布时间: $publish_datetime"
    python scripts/produce_with_gpt.py $resource_path
    python voice/clone.py
    python video/generate.py
    python xhs/publish.py "$publish_datetime"
done
