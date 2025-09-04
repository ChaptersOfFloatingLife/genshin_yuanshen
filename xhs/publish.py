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


def _find_first(driver, selectors, timeout=30):
    """Return the first element found by trying selectors in order.
    selectors: list of (By, value)
    Fails fast if none appear within timeout.
    """
    def _probe(d):
        for by, val in selectors:
            els = d.find_elements(by, val)
            if els:
                return els[0]
        return False

    return WebDriverWait(driver, timeout).until(_probe)


def publish_xiaohongshu(driver, scripts, publish_time="2025-01-12 16:00", video_path="output/video.mp4"):
    """发布小红书视频函数
    Args:
        driver: WebDriver实例
        scripts: 包含视频信息的字典
        publish_time: 发布时间
        video_path: 视频文件路径
    """
    time.sleep(3)

    video_path = os.path.abspath(video_path)
    print("开始上传文件", video_path)
    time.sleep(3)
    # ### 上传视频
    video = driver.find_element("xpath", '//input[@type="file"]')
    video.send_keys(video_path)

    # 填写标题（最多20个字符）
    content = scripts["content"]
    title_text = content.get("title")
    title_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@placeholder="填写标题会有更多赞哦～"]'))
    )
    title_input.clear()
    title_input.send_keys(title_text)

    time.sleep(1)
    # 填写描述（兼容新版编辑器）
    content_clink = _find_first(
        driver,
        [
            (By.CSS_SELECTOR, 'div.ql-editor[data-placeholder="输入正文描述，真诚有价值的分享予人温暖"]'),
            (By.CSS_SELECTOR, 'div[contenteditable="true"]'),
            (By.XPATH, '//div[@contenteditable="true"]')
        ],
    )
    info = content["title"]+"\n"+content["script"]+"\n"+scripts["content_extra"]+"\n"
    print(info)
    content_clink.send_keys(info) 
    
    time.sleep(3)
    # 标签
    for tag in scripts.get("tags", []):
        tag = "#" + tag
        # 保证焦点在编辑器内
        content_clink.click()
        content_clink.send_keys(tag)
        time.sleep(1)
        
        # 直接按回车键确认标签，再加一个空格断开
        content_clink.send_keys(Keys.ENTER)
        time.sleep(0.3)
        content_clink.send_keys(" ")
        time.sleep(0.2)

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
    input_time = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="选择日期和时间"]'))
    )
    # 解除只读并填写时间
    driver.execute_script('arguments[0].removeAttribute("readonly");', input_time)
    input_time.clear()
    input_time.send_keys(Keys.CONTROL, 'a')
    input_time.send_keys(Keys.DELETE)
    time.sleep(0.5)
    input_time.send_keys(publish_time)
    input_time.send_keys(Keys.TAB)
    time.sleep(1)

    # 等待发布按钮变为可点击状态
    publish_button = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((
            By.XPATH,
            '//span[contains(@class, "d-text") and text()="定时发布"]'
        ))
    )
    publish_button.click()
    print("已点击定时发布按钮")
    time.sleep(3)  # 等待发布完成

    print("视频发布完成！")

def publish_xhs_content(scripts_data, publish_time=None, video_path="output/video.mp4"):
    """Publish content to XHS programmatically.
    
    Args:
        scripts_data (dict): Content data with name, tags, content, etc.
        publish_time (str, optional): Publish time in format "2025-01-12 16:00"
        video_path (str): Path to the video file
        
    Returns:
        bool: True if successful, False otherwise
    """
    driver = None
    try:
        driver = get_driver()
        xiaohongshu_login(driver=driver)
        print("登录成功")

        print("Content data:", scripts_data)

        publish_xiaohongshu(driver, scripts_data, publish_time, video_path)
        return True

    except Exception as e:
        print(f"发布失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if driver:
            driver.quit()  # 退出浏览器


def main():
    # 检查是否提供了发布时间参数
    if len(sys.argv) != 2:
        print("使用方法: python publish.py '2025-01-12 16:00'")
        sys.exit(1)
    
    publish_time = sys.argv[1]
    print(publish_time)

    try:
        with open("output/script.json", "r", encoding="utf-8") as f:
            scripts = json.load(f)
        
        success = publish_xhs_content(scripts, publish_time)
        if not success:
            sys.exit(1)

    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()