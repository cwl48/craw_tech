# -*- coding: utf-8 -*-
import platform
import requests


def is_linux():
    sysstr = platform.system()
    print(sysstr)
    return sysstr == "Linux"


def get_proxy():
    return requests.get("http://127.0.0.1:8002/get/").content


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:8002/delete/?proxy={}".format(proxy))
