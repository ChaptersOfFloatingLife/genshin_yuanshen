import os
import time
import json

from liulanqi import COOKING_PATH, get_driver

XIAOHONGSHU_COOKING = os.path.join(COOKING_PATH, "xiaohongshu.json")

def save_current_cookies(driver):
    """获取并保存当前页面的 cookies"""
    # 确保页面已完全加载
    time.sleep(5)
    
    # 获取当前页面的所有 cookies
    cookies = driver.get_cookies()
    
    # 保存 cookies 到文件
    with open(XIAOHONGSHU_COOKING, 'w') as f:
        json.dump(cookies, f)
    
    return cookies

def manual_login_and_save_cookies():
    driver = get_driver()
    try:
        # 打开登录页面
        driver.get('https://creator.xiaohongshu.com/creator/post')
        
        # 等待手动登录完成
        input("请在浏览器中完成登录，然后按回车继续...")
        
        # 保存 cookies
        cookies = save_current_cookies(driver)
        print(f"已保存 {len(cookies)} 个 cookies")
        
    finally:
        driver.quit()

if __name__ == '__main__':
    manual_login_and_save_cookies()