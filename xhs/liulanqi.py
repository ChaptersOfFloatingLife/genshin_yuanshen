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

ROOT_PATH = os.getenv(
    "ROOT_PATH", "xhs_test")
VIDEO_PATH = os.path.join(ROOT_PATH, "output")
COOKING_PATH = os.path.join(ROOT_PATH, "cooking")

# Create directories if they don't exist
os.makedirs(ROOT_PATH, exist_ok=True)
os.makedirs(VIDEO_PATH, exist_ok=True)
os.makedirs(COOKING_PATH, exist_ok=True)

agent = 'Mozilla/5.0 (Macintosh; Linux) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
isDingShi = os.getenv("IS_DINGSHI", True)


def get_driver():
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
    print("链接上")
    return driver


def get_videos():
    """
    获取指定目录下的所有MP4视频文件，返回绝对路径
    
    Returns:
        list: 包含(文件绝对路径, 文件名)元组的列表
    """
    try:
        mp4_result = []
        path = pathlib.Path(VIDEO_PATH).resolve()  # 转换为绝对路径
        
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
        print(f"错误：目录 {VIDEO_PATH} 不存在")
        sys.exit(1)


def get_publish_date(title, index):
    # 代表的是 加一天时间
    time_long = int(index/3) * 24
    now = datetime.datetime.today()
    if(now.hour > 20):
        time_long = 24
    tomorrowemp = now + datetime.timedelta(hours=time_long)
    print("title:", title)
    # 暂时注释掉+ datetime.timedelta(hours = 24)
    if title.find("(1)") > 0 or title.find("(4)") > 0 or title.find("(7)") > 0:
        tomorrow = tomorrowemp.replace(hour=8, minute=0, second=0)
    elif title.find("(2)") > 0 or title.find("(5)") > 0:
        tomorrow = tomorrowemp.replace(hour=12, minute=0, second=0)
    elif title.find("(3)") > 0 or title.find("(6)") > 0:
        tomorrow = tomorrowemp.replace(hour=18, minute=0, second=0)
    print("准备写入的时间是:", tomorrow)
    if(tomorrow <= now):
        tomorrow = now + \
            datetime.timedelta(hours=2) + datetime.timedelta(hours=1*index)
    print("输出的时间是:", tomorrow.strftime("%Y-%m-%d %H:%M"))
    return tomorrow.strftime("%Y-%m-%d %H:%M")
