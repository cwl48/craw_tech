import requests
import sys
import html2text
from flask import Flask, request
import urllib.parse

app = Flask(__name__)

h = html2text.HTML2Text()
# html to markdown


@app.route('/html2Markdown')
def getpicurl():

    url = request.args.get('url')
    res = requests.get(url).json()
    if res['s'] != 1:
        return ''
    s = res['d']['content']
    r = h.handle(s)
    return r


def init():
    app.run(host='0.0.0.0', port=8001, debug=False)
