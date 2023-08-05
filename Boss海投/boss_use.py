from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

url = 'https://www.zhipin.com/web/geek/job?query=java&city=101020100&experience=102'
header = 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
css = ".job-card-wrapper:nth-child(1) .job-area"

with open('Boss_cookies', 'r') as f:
    cookies = json.load(f)


def use(url,cookies,header):
    options = webdriver.ChromeOptions()
    options.add_argument(header)
    driver = webdriver.Chrome(options=options)
    driver.get(url)	
    for cookie in cookies:
        driver.add_cookie(cookie)
    print("成功读取到对应的cookie文件，完成登录")
    time.sleep(5)
    for i in range(1, 31):
        css_selector = f".job-card-wrapper:nth-child({i}) .job-area"
        driver.find_element(By.CSS_SELECTOR, css_selector).click()
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[1])
        if len(driver.find_elements(By.LINK_TEXT, "继续沟通")) == 0:
            driver.find_element(By.LINK_TEXT, "立即沟通").click()
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    input("...")

use(url,cookies,header)