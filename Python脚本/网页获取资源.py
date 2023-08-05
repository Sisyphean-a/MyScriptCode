import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

search_term = input("请输入您要搜索的关键字: ")
search_term = quote_plus(search_term)

urls = [
    {
        "url": "https://www.ghxi.com/?s={}".format(search_term),
        "result_selector": "#wrap > div > div > div > div.sec-panel-body > ul.post-loop.post-loop-default",
        "link_selector": "#wrap > div > div > div > div.sec-panel-body > ul.post-loop.post-loop-default > li > div.item-content > h2 > a"
    },
    {
        "url": "https://tmioe.com/?s={}".format(search_term),
        "result_selector": "#wrap > div > div > div > div.sec-panel-body > ul.post-loop.post-loop-default",
        "link_selector": "#wrap > div > div > div > div.sec-panel-body > ul.post-loop.post-loop-default > li> div.item-content> h2> a"
    },
    {
        "url": "https://www.lan-sha.com/?s={}".format(search_term),
        "result_selector": "#app> main> div> div.post-main> div> ul",
        "link_selector": "#app> main> div> div.post-main> div> ul> li> div> div.post-item-main> h2> a"
    }
]

for url in urls:
    response = requests.get(url["url"])
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.select(url["result_selector"])
    for result in results:
        links = result.select(url["link_selector"])
        for link in links:
            title = link.text.strip()
            href = link['href']
            print("标题: {}\n网址: {}\n\n---{}---\n".format(title, href, '-'*30))
    input("Please ......")