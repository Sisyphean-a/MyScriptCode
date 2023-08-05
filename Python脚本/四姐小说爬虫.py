import requests
from bs4 import BeautifulSoup
import threading


li_num = 1000
results = [None] * li_num

# base_url = 'https://www.52shuku.vip/yanqing/b/bjNgT.html'
base_url = 'https://www.52shuku.vip/yanqing/b/bjP6F.html'
base_url = base_url.replace('.html', '_{}.html')


selector = '#text'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Content-Type': 'text/html; charset=UTF-8'
}

# 定义init函数
def init(url):
    response = requests.get(url, headers=HEADERS)
    response.encoding = 'UTF-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    text_div = soup.select_one(selector)
    return text_div


# 定义爬取函数
def crawl(base_url,li_num):
    for i in range(2, li_num+2):
        try:
            # 获取页面内容
            url = base_url.format(i)
            # 获取文本内容
            text_div = init(url)
            text = '\n'.join(p.text for p in text_div.find_all('p'))
            # 将文本写入文件
            with open("output.txt", 'a', encoding='utf-8') as f:
                f.write(text + '\n')
            print("爬取到第" + str(i-1) + "页")
        except AttributeError as e:
            if f >= 20:
                print(f"结束了，当前f={f}")
            else:
                print(f"出现异常，当前f={f}")
            break

# 定义入口函数
if __name__ == '__main__':
    crawl(base_url,li_num)
