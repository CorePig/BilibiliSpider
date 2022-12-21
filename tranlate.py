import requests

import json


def trans():
    txt = input("请输入要翻译的内容：")
    data = {
        "i": txt,
        "from": "zh-CHS",
        "to": "ja",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTIME",
        "strict":"true"
    }
    # url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
    url = "http://fanyi.youdao.com/translate?"
    res = requests.post(url, data=data)
    js = res.json()
    print("翻译结果：", js['translateResult'][0][0]['tgt'])


if __name__ == '__main__':
    while True:
        trans()