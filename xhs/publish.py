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

from liulanqi import COOKING_PATH, get_driver, get_videos


XIAOHONGSHU_COOKING = os.path.join(COOKING_PATH, "xiaohongshu.json")


def xiaohongshu_login(driver):
    """小红书登录函数"""
    if (os.path.exists(XIAOHONGSHU_COOKING)):
        print("cookies存在")
        with open(XIAOHONGSHU_COOKING) as f:
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
    else:
        print("cookies不存在")
        driver.get('https://creator.xiaohongshu.com/creator/post')
        driver.find_element(
            "xpath", '//*[@placeholder="手机号"]').send_keys("15624965741")
        # driver.find_element(
        #     "xpath", '//*[@placeholder="请输入密码"]').send_keys("")
        driver.find_element(
            "xpath", '//*[@placeholder="验证码"]').send_keys("123456")

        driver.find_element("xpath", '//button[text()="登 123录"]').click()
        print("等待登录")
        time.sleep(30)
        print("登录完毕")
        cookies = driver.get_cookies()
        with open(XIAOHONGSHU_COOKING, 'w') as f:
            f.write(json.dumps(cookies))
        print(cookies)
        time.sleep(1)


def publish_xiaohongshu(driver, mp4, index):
    """发布小红书视频函数
    Args:
        driver: WebDriver实例
        mp4: 包含视频路径和标题的元组
        index: 视频序号
    """
    time.sleep(3)
    # driver.get("https://creator.xiaohongshu.com/publish/publish?from=menu")
    # driver.find_element("xpath", '//*[text()="发布笔记"]').click()
    print("开始上传文件", mp4[0])
    time.sleep(3)
    # ### 上传视频
    video = driver.find_element("xpath", '//input[@type="file"]')
    video.send_keys(mp4[0])

    # 填写标题
    content = mp4[1].replace('.mp4', '')
    driver.find_element(
        "xpath", '//*[@placeholder="填写标题会有更多赞哦～"]').send_keys(content)

    time.sleep(1)
    # 填写描述
    content_clink = driver.find_element(
        By.CSS_SELECTOR, 
        'div.ql-editor[data-placeholder="输入正文描述，真诚有价值的分享予人温暖"]'
    )
    content_clink.send_keys(content)

    # time.sleep(3)
    # # #虐文推荐 #知乎小说 #知乎文
    # for label in ["#虐文","#知乎文"]:
    #     content_clink.send_keys(label)
    #     time.sleep(1)
    #     data_indexs = driver.find_elements(
    #         "class name", "publish-topic-item")
    #     try:
    #         for data_index in data_indexs:
    #             if(label in data_index.text):
    #                 print("点击标签",label)
    #                 data_index.click()
    #                 break
    #     except Exception:
    #         traceback.print_exc()
    #     time.sleep(1)

    # 定时发布按钮定位
    dingshi = driver.find_element(
        By.XPATH, 
        '//span[contains(@class, "el-radio__label") and text()="定时发布"]'
    )
    time.sleep(2)
    print("点击定时发布")
    # 使用 JavaScript 执行点击，而不是直接点击
    driver.execute_script("arguments[0].click();", dingshi)

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
    input_time.send_keys("2025-01-12 16:00")  # 输入新时间
    time.sleep(2)

    # 等待发布按钮变为可点击状态
    publish_button = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((
            By.XPATH,
            '//span[contains(@class, "d-text") and text()="定时发布"]'
        ))
    )
    publish_button.click()
    print("已点击定时发布按钮")
    time.sleep(3)  # 等待发布完成

    print("视频发布完成！")

# 主程序入口
if __name__ == "__main__":
    try:
        driver = get_driver()
        xiaohongshu_login(driver=driver)
        print("登录成功")
        mp4s = get_videos()
        print(mp4s)
        for index, mp4 in enumerate(mp4s):
            publish_xiaohongshu(driver, mp4, index)
            time.sleep(10)
    finally:
        # driver.quit()  # 退出浏览器
        pass