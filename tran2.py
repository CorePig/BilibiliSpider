# 百度通用翻译API,不包含词典、tts语音合成等资源，如有相关需求请联系translate_api@baidu.com
# coding=utf-8

import http.client
import hashlib
import time
import urllib
import random
import json
import re
from pip._vendor.distlib.compat import raw_input
# q为要翻译的字符串
def tran(q):
    # 百度appid和密钥需要通过注册百度【翻译开放平台】账号后获得
    appid = '20220619001251976'  # 填写你的appid
    secretKey = '19t71Tv8RpJRnGZVRLlu'  # 填写你的密钥

    httpClient = None
    myurl = '/api/trans/vip/translate'  # 通用翻译API HTTP地址

    fromLang = 'en'  # 原文语种
    toLang = 'jp'  # 译文语种
    salt = random.randint(32768, 65536)
    # 手动录入翻译内容，q存放
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + \
            '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    # 建立会话，返回结果
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)

        # print(result)
        # 翻译成功返回翻译后的结果
        if result['trans_result']:
            return result['trans_result'][0]['dst']
        # 翻译失败返回
        else:
            return "翻译失败！"

    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()
if __name__=="__main__":
    '''
    用的时候dic替换成你的Json数据即可
    最后的ans是一个字符串类型
    '''
    n=int(input("请输入数据行数："))
    s=[input().strip(";") for i in range(n)]
    # 拼接
    flag=True
    temps=""
    for i in s:
        if not flag:
            temps+=f",{i}"
        else:
            temps+="{"+i
            flag=False
    temps+="}"
    temps=temps.replace("：",":")
    temps=temps.replace("“",'"')
    temps=temps.replace("”",'"')
    # print(temps)
    dic=json.loads(temps)
    # print(dic)


    # 要翻译的字典值
    # dic = {"hello":"Hello"
    #     ,"eat": "eat"
    #     , "look": "look"}
    # 把字典的值转化成小写
    dic={i:dic[i].lower() for i in dic}
    for i in dic:
        if dic[i]:
            dic[i]=tran(dic[i])
            time.sleep(1)
    # 去括号
    ans=str(dic)
    ans=ans.replace("{","")
    ans=ans.replace("}","")
    ans=ans.replace(",",";\n")
    ans=ans.replace(" ","")
    ans=ans.replace("'",'"')
    print(ans)