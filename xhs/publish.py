import os
import time
import json
import traceback
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

from liulanqi import get_driver


def xiaohongshu_login(driver):

    cookies_file = "cookies/xiaohongshu.json"
    """小红书登录函数"""
    print("开始加载cookie")
    with open(cookies_file) as f:
        cookies = json.loads(f.read())
        driver.get("https://creator.xiaohongshu.com/creator/post")
        driver.implicitly_wait(10)
        driver.delete_all_cookies()
        time.sleep(2)
        # 遍历并添加cookie
        print("加载cookie")
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie["expiry"]
            driver.add_cookie(cookie)
        time.sleep(2)
        # 刷新
        print("开始刷新")
        driver.refresh()
        driver.get("https://creator.xiaohongshu.com/publish/publish")
        time.sleep(2)


def publish_xiaohongshu(driver, scripts, publish_time="2025-01-12 16:00"):
    """发布小红书视频函数
    Args:
        driver: WebDriver实例
        mp4: 包含视频路径和标题的元组
        index: 视频序号
    """
    time.sleep(3)

    video_path="output/video.mp4"
    video_path = os.path.abspath(video_path)
    print("开始上传文件", video_path)
    time.sleep(3)
    # ### 上传视频
    video = driver.find_element("xpath", '//input[@type="file"]')
    video.send_keys(video_path)

    # 填写标题
    # content = scripts.get("name", "")
    # driver.find_element(
    #     "xpath", '//*[@placeholder="填写标题会有更多赞哦～"]').send_keys(content)
    content = scripts["content"]

    time.sleep(1)
    # 填写描述
    content_clink = driver.find_element(
        By.CSS_SELECTOR, 
        'div.ql-editor[data-placeholder="输入正文描述，真诚有价值的分享予人温暖"]'
    )
    info = content["title"]+"\n"+content["script"]+"\n"+scripts["content_extra"]+"\n"
    print(info)
    content_clink.send_keys(info) 
    
    time.sleep(3)
    # 标签
    for tag in scripts.get("tags", []):
        tag = "#" + tag
        content_clink.send_keys(tag)
        time.sleep(1)
        
        # 直接按回车键确认标签
        content_clink.send_keys(Keys.ENTER)
        time.sleep(0.5)  # 给一点时间让标签完成添加

    # 定时发布按钮定位
    schedule_button = driver.find_element(
        By.XPATH, 
        '//span[contains(@class, "el-radio__label") and text()="定时发布"]'
    )
    time.sleep(2)
    print("点击定时发布")
    # 使用 JavaScript 执行点击，而不是直接点击
    driver.execute_script("arguments[0].click();", schedule_button)

    time.sleep(5)
    # 找到时间输入框并输入时间
    input_time = driver.find_element(
        By.XPATH, 
        '//input[@placeholder="选择日期和时间"]'
    )
    # 清除默认值
    input_time.clear()  # 先清除
    input_time.send_keys(Keys.CONTROL, 'a')  # 再次全选以确保清除
    input_time.send_keys(Keys.DELETE)  # 删除所有内容
    time.sleep(1)  # 等待清除完成
    input_time.send_keys(publish_time)  # 输入新时间
    time.sleep(1)

    # 等待发布按钮变为可点击状态
    publish_button = WebDriverWait(driver, 1000).until(
        EC.element_to_be_clickable((
            By.XPATH,
            '//span[contains(@class, "d-text") and text()="定时发布"]'
        ))
    )
    publish_button.click()
    print("已点击定时发布按钮")
    time.sleep(3)  # 等待发布完成

    print("视频发布完成！")

def main():
    # 检查是否提供了发布时间参数
    if len(sys.argv) != 2:
        print("使用方法: python publish.py '2025-01-12 16:00'")
        sys.exit(1)
    
    publish_time = sys.argv[1]
    print(publish_time)

    try:
        driver = get_driver()
        xiaohongshu_login(driver=driver)
        print("登录成功")

        with open("output/script.json", "r", encoding="utf-8") as f:
            scripts = json.load(f)
        print(scripts)

        publish_xiaohongshu(driver, scripts, publish_time)

    finally:
        driver.quit()  # 退出浏览器

if __name__ == "__main__":
    main()