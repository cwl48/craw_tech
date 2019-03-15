import requests
import sys
import html2text
from flask import Flask, request
import urllib.parse
from base import scheduled
import html
from bs4 import BeautifulSoup

app = Flask(__name__)

h = html2text.HTML2Text()
# html to markdown


@app.route('/html2Markdown')
def getpicurl():

    third_type = request.args.get('thirdType')
    url = request.args.get('url')
    third_type = int(third_type)
    if third_type == 1:
        return juejin(url)
    if third_type == 10:
        return segment(url)
    return ""


def juejin(url):

    res = requests.get(url).json()
    if res['s'] != 1:
        return ''
    s = res['d']['content']
    r = h.handle(s)
    return r


def segment(url):
    res = requests.get(url)
    # html文档
    htmls = res.text
    soup = BeautifulSoup(htmls, 'html.parser')

    article = soup.find("div", class_="article__content")
    imgList = article.find_all("img")
    for img in imgList:
        url_str = "https://www.chaoyer.com/csy/common/file/proxy?proxy=1&img=https://segmentfault.com" + str(
            img["data-src"])
        img["src"] = url_str
    s = article.prettify()
    r = h.handle(s)
    return r


def init():
    scheduled.start(app)
    app.run(host='0.0.0.0', port=8001, debug=False)
