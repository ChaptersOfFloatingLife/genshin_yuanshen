# Copied from
# https://github.com/menhuan/notes/blob/master/python/douyin/upload_xiaohongshu.py

import datetime
from operator import index
import traceback
from selenium import webdriver

from time import sleep

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import selenium
from selenium import webdriver
import pathlib
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import json
import os
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
import sys



def get_driver():
    agent = 'Mozilla/5.0 (Macintosh; Linux) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-automation'])
    chrome_options.add_argument(f'user-agent={agent}')
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled")
    # driver = webdriver.Remote(
    #     command_executor="http://101.43.210.78:50000",
    #     options=chrome_options
    # )
    driver = webdriver.Chrome(options=chrome_options)

    driver.maximize_window()
    print("开始运行浏览器")
    return driver


def get_videos(video_path="output"):
    """
    获取指定目录下的所有MP4视频文件，返回绝对路径
    
    Returns:
        list: 包含(文件绝对路径, 文件名)元组的列表
    """
    try:
        mp4_result = []
        path = pathlib.Path(video_path).resolve()  # 转换为绝对路径
        
        for video_path in path.iterdir():
            if video_path.suffix.lower() == '.mp4':
                # 使用 resolve() 获取绝对路径
                absolute_path = str(video_path.resolve())
                mp4_result.append((absolute_path, video_path.name))

        if mp4_result:
            print("检查到视频路径：", mp4_result)
        else:
            print("未检查到视频路径，程序终止！")
            sys.exit(1)
            
        return sorted(mp4_result)
        
    except FileNotFoundError:
        print(f"错误：目录 {video_path} 不存在")
        sys.exit(1)