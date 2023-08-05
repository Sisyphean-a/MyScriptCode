from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

url_login = 'https://www.zhipin.com/web/user/?ka=header-login'
url_select = 'https://www.zhipin.com/web/geek/job?query=java&city=101020100&experience=102'
header = 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'



def login(url_login, url_select,header):
    options = webdriver.ChromeOptions()
    options.add_argument(header)
    driver = webdriver.Chrome(options=options)
    driver.get(url_login)
    element = driver.find_element(By.XPATH,'//*[@id="wrap"]/div/div[2]/div[2]/div[2]/div[1]/div[4]/a')
    element.click()
    time.sleep(2)
    while True:
        if driver.current_url != url_login:
            time.sleep(3)
            driver.get(url_select)
            break
    cookies = driver.get_cookies()
    
    with open('Boss_cookies', 'w') as f:
        json.dump(cookies, f)
    print("写入Cookie文件成功")
    
    input("回车结束运行")


login(url_login, url_select,header)
