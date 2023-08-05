import requests
from bs4 import BeautifulSoup
import threading
from concurrent.futures import ThreadPoolExecutor
import time

selector = '#text'


def get_page_num(url):
    # 获取章节数目
    selector_li = 'body > section > div > div > article > ul'
    soup = init(url, selector_li)
    li = soup.find_all("li")
    num = len(li)
    print(f"目标网址共{num}章")
    return num


def get_article_title(url):
    # 获取小说标题
    selector_title = 'body > section > div > div > header > h1'
    soup = init(url, selector_title)
    return soup.text


# 定义init函数
def init(url, selector):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Content-Type': 'text/html; charset=UTF-8'
    }
    try:
        response = requests.get(url, headers=HEADERS)
        response.encoding = 'UTF-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        text_div = soup.select_one(selector)
        return text_div
    except requests.exceptions.SSLError as e:
        # 处理SSLError异常
        print(f"出现SSLError异常: {e}")
    except requests.exceptions.ProxyError as e:
        # 处理ProxyError异常
        print(f"出现ProxyError异常: {e}")


def crawl_page(i):
    # 读取网页目标内容
    global selector
    try:
        # 获取页面内容
        url = base_url.format(i)
        text_div = init(url, selector)
        if not text_div:
            selector = '#nr1'
            text_div = init(url, selector)
        # 获取文本内容
        text = '\n'.join(p.text for p in text_div.find_all('p'))
        # 保存结果
        results[i - 2] = text
        print(f"success : {i}")
    except AttributeError as e:
        print(f"error : {i}  异常信息为：{e}\n")


def write_txt(article_title):
    # 把目标内容写入文件
    title = article_title + ".txt"
    with open(title, 'w', encoding='utf-8') as f:
        for text in results:
            if text is not None:
                f.write(text + '\n')


def start_thread(article_title):
    # 创建一个包含64个线程的线程池
    with ThreadPoolExecutor(max_workers=64) as executor:
        # 提交任务到线程池
        for i in range(2, li_num + 2):
            executor.submit(crawl_page, i)

    # 将结果写入文件
    write_txt(article_title)
    print("爬取完成")



# 定义入口函数
if __name__ == '__main__':
    # url = 'https://www.52shuku.vip/yanqing/hxoP.html'
    url = 'https://www.52shuku.vip/chongsheng/2420.html'
    # url = input("请输入目标网址：")
    base_url = url.replace('.html', '_{}.html')

    start_time = time.perf_counter()

    article_title = get_article_title(url)
    li_num = get_page_num(url)

    results = [None] * li_num
    start_thread(article_title)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"程序运行时间: {elapsed_time:.6f}秒")
