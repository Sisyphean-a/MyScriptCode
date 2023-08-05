import os
import re

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Content-Type': 'text/html; charset=UTF-8'
}

URL = 'https://www.biqugehxs.com/allbook_14186_5.html'
select_allBook_list = 'body > div.container > div.row > div > div:nth-child(1) > dl > dt > a'

# URL_INIT = 'https://www.biqugehxs.com/html/dayinxia/'
# URL_INIT = 'https://www.biqugehxs.com/html/yuzhiyuan/'
# URL_INIT = 'https://www.biqugehxs.com/html/jiemeijiandejiaoliang/'
# URL_INIT = 'https://www.biqugehxs.com/html/weiliaoshijieheping_wozhinenshangliaomama/'
URL_INIT = 'https://www.biqugehxs.com/html/dainverjiademiyuefengbo/'
# URL_INIT = 'https://www.biqugehxs.com/html/mamadejururenqiguimi/'
# URL_INIT = 'https://www.biqugehxs.com/html/daizhoumeiyanyimuchuangmoshi/'

select_text = '#content > div'
select_list = 'body > div.container > div.row.row-section > div > div:nth-child(4) > ul'
select_title = '#container > div > div > div.reader-main > h1'


def replace_str(s):
    """
    :param s: 待处理的字符串
    :return: 替换后的字符串
    """
    s = s.replace('<div align="center">', '')
    s = s.replace('<br/>\n<br/>\n', '\n')
    s = s.replace('<br>', '')
    s = s.replace("<br/>", "")
    s = s.replace("\n\n", "\n")
    s = s.replace("\n", "")
    s = s.replace("    ", " ")
    s = s.replace("　　", "\n")
    s = s.replace("\n\n", "\n")
    s = s.replace("\n\n", "\n")
    s = s.replace('<!--script language="javascript" type="text/javascript" src="/css/js/txt.js"></script>', '')
    s = s.replace('<script language="javascript">', '')
    s = s.replace('</script--></br></div>', '')
    s = re.sub(r'sjwzl\(".*?"\)', '', s)
    return s


def initialize_soup(url, headers=None):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content.decode("gbk"), 'html.parser')
    return soup


def get_title(url, select, headers=None):
    """
    获取网页标题
    :param url: str，请求网页的Url
    :param select: str，BeautifulSoup解析网页的CSS选择器，用于获取指定的HTML元素
    :param headers: dict，请求头，默认值为None
    :return: str，网页的标题
    """
    soup = initialize_soup(url, headers=headers)
    title = soup.select_one(select).text.strip()
    replace_str(title)
    return title


def get_number_list(url, select):
    """根据给定的URL和CSS选择器获取页面链接中的数字列表。
    :param url: 需要获取信息的网页的URL
    :param select:用于选择需要获取的CSS选择器
    :return: 页面链接中的数字列表
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for item in soup.select(select):
        for link in item.find_all('a'):
            href = link.get('href')
            href = re.sub('\D', '', href) if href else ''
            links.append(href)
    return links


def get_text(url, select, headers=None):
    """根据指定的URL和CSS选择器获取网页文本内容，并进行格式化处理。
    :param url: 需要获取信息的网页URL。
    :param select: 用于选择需要获取内容的CSS选择器。
    :param headers: HTTP请求头信息。默认为None。
    :return: 经过格式化的网页文本内容。
    """
    soup = initialize_soup(url, headers=headers)
    content = soup.select_one(select)
    target_str = str(content)
    formatted_str = replace_str(target_str)
    return formatted_str


def write_to_many_file(string, name):
    """将字符串写入多个文件
    :param string: 要写入文件的字符串
    :param name: 文件名
    :return: 无返回值
    """
    folder = './param_dir'
    if not os.path.isdir(folder):
        os.makedirs(folder)
    name = name + ".txt"
    path = os.path.join(folder, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(string)


def write_to_one_file(string, name):
    """将字符串写入单个文件
    :param string: 要写入文件的字符串
    :param name: 文件名
    :return: 无返回值
    """
    folder = './param_dir'
    if not os.path.isdir(folder):
        os.makedirs(folder)
    dir_name = name.split("【")[1].split("】")[0] + ".txt"
    path = os.path.join(folder, dir_name)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(name)
        # f.write('\n')
        f.write(string)


def scrape_page(url, select_title, select_text, headers):
    """这个函数用来爬取网页内容并将特定区域的标题和文本写入到一个文件中
    :param url: 爬取内容的网页地址
    :param select_title: 用来匹配页面中标题的 CSS 选择器
    :param select_text: 用来匹配页面中文本的 CSS 选择器
    :param headers: HTTP 请求头部信息，用于模拟人类浏览器操作
    """
    title = get_title(url, select_title, headers)
    test = get_text(url, select_text, headers)
    write_to_one_file(test, title)
    print(title)


if __name__ == '__main__':
    links = get_number_list(URL_INIT, select_list)
    print(links)
    for i in links:
        url = URL_INIT + i + '.html'
        scrape_page(url, select_title, select_text, HEADERS)
