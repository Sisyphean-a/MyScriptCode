import requests
from bs4 import BeautifulSoup


def get_div(target, page=1):
    # 初始化页面，获取div节点
    url = f'https://www.52shuku.vip/so/search.php?q={target}&m=&f=_all&s=&p={page}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    div = soup.select('body > section > div > div')[0]
    return div


def search_num(div):
    # 获取搜索结果个数
    num_results = int(div.select('div > b')[0].text)
    return num_results


def search_article(div, num):
    # 获取目标网址和标题
    lists = []
    for i in range(2, num + 2):
        if i > 11:
            break
        # print(i)
        article = div.select(f'article:nth-child({i})')[0]
        try:
            a = article.select('header > h2 > a')[0]
        except IndexError as a:
            print("其实并没有结果...")
            break
        href = a['href']
        title = a.select('h4')[0].text
        lists.append({'href': href, 'title': title})
    if lists is not []:
        format_results(lists)
    return lists


def format_results(results):
    # 输出最终信息
    for result in results:
        print(f"\nTitle: {result['title']}")
        print(f"URL: {result['href']}\n")


if __name__ == '__main__':
    # Example usage
    target = input("请输入搜索内容：")
    div = get_div(target)

    # 获取目标节点个数
    num = int(div.select('div > b')[0].text)
    print(f"共搜出{num}条结果")

    results = []

    if num <= 10:
        results.extend(search_article(div, num))
    elif 10 < num <= 20:
        results.extend(search_article(div, 10))
        div = get_div(target, 2)
        results.extend(search_article(div, num - 10))
    if num > 20:
        results.extend(search_article(div, 10))
        div = get_div(target, 2)
        results.extend(search_article(div, 10))
        div = get_div(target, 3)
        results.extend(search_article(div, num - 20))
