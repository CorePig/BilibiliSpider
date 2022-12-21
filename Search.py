'''
#本包是进行数据爬取的包，爬取到的数据会存进该目录下的弹幕池内

#up主的个人信息
https://api.bilibili.com/x/space/acc/info?mid=【UserUid】&jsonp=jsonp

# b 站up主的主页
https://space.bilibili.com/66607740/?spm_id_from=333.999.0.0

# 获取Up主的上传的所有视频信息
https://api.bilibili.com/x/space/arc/search?mid=【UserUid】

# 获取视频的cid（将bvid后面的编码替换为对应视频的编码即可）
https://api.bilibili.com/x/player/pagelist?bvid=BV1ji4y1U7UC&jsonp=jsonp

# 弹幕爬取的api
https://comment.bilibili.com/132373554.xml
'''
# video
import subprocess

import requests
import re
import csv
import sys
import os
from multiprocessing import Pool
from pymongo import MongoClient
from Logs import *
import json
import threading



# 创建一个链接
client = MongoClient()
# 连接到mydata数据库
database = client['mydata']
# 使用表msg进行存储
tables = database['msg']
# -----------------------------存数据库------------------------------------#
def saveMongo(lists):
    tables.insert_many(lists)
# -----------------------------请求代码区-----------------------------------#

# 总业务(执行完毕的话返回UP主的id与True,否则返回''与False)
def AllOpe(url):
    try:
        r'''(?x)\A
        ([a-z][a-z0-9+\-.]*)://　　　　　　　　　　　　　# Scheme
        ([a-z0-9\-._~%]+　　　　　　　　　　　　　　　　　# IPv4 host
        |\[[a-z0-9\-._~%!$&'()*+,;=:]+\])　　　　　　　# IPv6 host
        (:[0-9]+)?　　　　　　　　　　　　　　　　　　　　　# Port number
        ([a-zA-Z0-9\-\/._~%!$&'()*+]+)?　　　　　　　　# path
        (\?[a-zA-Z0-9&=]+)?　　　　　　　　　　　　　　　　# query
        '''
        if not url:
            return '', False
            # 先对url进行解析（提取出博主的信息、博主名下视频的信息）
        t = re.findall(
            r'''(?x)\A([a-z][a-z0-9+\-.]*)://([a-z0-9\-._~%]+|\[[a-z0-9\-._~%!$&'()*+,;=:]+\])(:[0-9]+)?([a-zA-Z0-9\-\/._~%!$&'()*+]+)?(\?[a-zA-Z0-9&=]+)?''',
            url)[0][3]
        # 解析url中的path路径
        # t=re.findall('/(.*)[/?]',t)
        t = re.findall('/([0-9]{5,10})', t)

        # 正常的path只有一个值，就是up主的id
        if len(t) != 1:
            return "", False
        log.info(f"用户{t[0]}的视频与弹幕开始收集！")
        lis = getBvidList(t[0])

        # # 最后爬取弹幕并存储
        # 开启一个大小为5的线程池
        po = Pool(5)
        po.map(GetBarrage, lis)
        return t[0], True
    except Exception as e:
        print(e)
        return '系统出错!', False


# 给出用户id获取用户名下的视频aid与bvid还有视频名
def getBvidList(userid):
    # 发送请求
    temp = requests.get(f"https://api.bilibili.com/x/space/arc/search?mid={userid}").content.decode("utf-8")

    # 解析网页（抓大）
    temp = re.findall('"vlist"(.*?)"page"', temp)

    # 解析网页（抓小）
    temp = re.findall('"title"."(.*?)".*?,"mid":(.*?),.*?,"aid":(.*?)"bvid".*?"(.*?)"', temp[0])
    # 这里的temp是一个元组列表，列属性为视频标题、视频作者id、视频aid、bvid
    # 每一行为一个视频数据
    return temp


# 根据视频信息爬取该视频下的弹幕然后进行存储
'''
<d p="831.56800,1,25,16777215,1653293349,0,d2822718,1058660364662753792,11">领克：台词不到位 !重说一遍！</d>
参数1（831.56800）：弹幕出现的时间，以秒数为单位
参数2（1）：弹幕的模式，1-3 滚动弹幕，4 底端弹幕，5顶端弹幕，6 逆向弹幕，7 精准定位，8 高级弹幕
参数3（25）：字号 （12非常小，16特小，18小，25中，36大，45很大，64特别大）
参数4（16777215）：字体的颜色；这串数字是十进制表示；通常软件中使用的是十六进制颜色码；
           e.g:
            白色
            RGB值：(255,255,255)
            十进制值：16777215
            十六进制值：#FFFFFF
参数5（1653293349）：unix时间戳，从1970年1月1日（UTC/GMT的午夜）开始所经过的秒数
参数6（0）：弹幕池，0普通池，1字幕池，2特殊池 【目前特殊池为高级弹幕专用】
参数7（d2822718）：发送者的ID，用于“屏蔽此弹幕的发送者”功能
参数8（1058660364662753792）：弹幕在弹幕数据库中rowID 用于“历史弹幕”功能。
'''
def downloadaudio(vpath,url,name):
    log.info(f"视频{name}的声音开始爬取...")
    # 请求头
    headers = {
        'referer': 'https://www.bilibili.com/video/BV1N5411Q75n?spm_id_from=333.1007.extension.content.click',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63'}
    audio=requests.get(url,headers=headers).content
    with open(f"{vpath}\\{name}声音.mp3","wb") as f1:
        f1.write(audio)
    log.info(f"视频{name}的声音爬取完毕...")


def downloadvideo(vpath,url,name):
    log.info(f"视频{name}的视频开始爬取...")
    # 请求头
    headers = {
        'referer': 'https://www.bilibili.com/video/BV1N5411Q75n?spm_id_from=333.1007.extension.content.click',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63'}
    video = requests.get(url, headers=headers).content
    with open(f"{vpath}\\{name}视频.mp4","wb") as f2:
        f2.write(video)
    log.info(f"视频{name}的视频爬取完毕...")

def saveanddelMP4(vpath,name):
    log.info(f"视频{name}的声音与视频开始合成...")
    cmd = f'D:/apache-tomcat-9.0.53-windows-x64/ffpmeg/ffpmeg/bin/win64/ffmpeg.exe -i {vpath}\\{name}视频.mp4 -i {vpath}\\{name}声音.mp3 -c:v copy -c:a aac -strict experimental {vpath}\\{name}.mp4'
    subprocess.run(cmd)
    log.info(f"视频{name}的声音与视频合成完毕...")

# # 跳板
# def SpringBoard():

def download(vpath,name,audio_url,video_url):
    name = re.sub('[\/:*?"<>|]', '_', name)  # 去掉非法字符
    name=name.replace('\\','')
    name=name.replace(" ","")
    name=name.replace("-","_")
    thls=[]
    t1=threading.Thread(target=downloadaudio,args=(vpath,audio_url,name))
    t2=threading.Thread(target=downloadvideo,args=(vpath,video_url,name))
    thls.append(t1)
    thls.append(t2)
    for i in thls:
        i.start()
        i.join()

    # 以上两个子线程结束后再进行以下运行
    t3=threading.Thread(target=saveanddelMP4,args=(vpath,name))
    t3.start()
    t3.join()
    log.info(f"视频{name}临时文件开始删除...")
    os.remove(f"{vpath}\\{name}视频.mp4")
    os.remove(f"{vpath}\\{name}声音.mp3")
    log.info(f"视频{name}临时文件删除完毕...")



def GetBarrage(col):
    # 进行数据的存储
    mpath = f"{sys.path[0]}\\弹幕池\\{col[1]}"
    vpath = f"{sys.path[0]}\\视频池\\{col[1]}"
    # 判断路径是否存在，不存在创建
    if not os.path.exists(mpath):
        os.makedirs(mpath)
    if not os.path.exists(vpath):
        os.makedirs(vpath)
    log.info(f"开始爬取视频{col[0]}的弹幕...")
    # col是一个元组，按照顺序应包含以下三个属性
    # 视频标题、作者mid、aid、bvid
    # 对应在本函数的功能就是作为文件名存弹幕文件、UP主所有弹幕文件夹名称、...、获取视频的cid

    # 请求头
    headers = {
        'referer': 'https://www.bilibili.com/video/BV1N5411Q75n?spm_id_from=333.1007.extension.content.click',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63'}
    # 获取该视频的视频与声音url
    html = requests.get(
        f'https://www.bilibili.com/video/{col[3]}?spm_id_from=333.1007.extension.content.click').content.decode(
        'utf-8')
    try:
        ans = json.loads(re.findall('<script>window.__playinfo__=(.*?)</script>', html)[0])
        # pprint.pprint(ans)
        audio_url = ans['data']['dash']['audio'][0]['baseUrl']
        video_url = ans['data']['dash']['video'][0]['base_url']
        # print(audio_url)
        # print(video_url)
        download(vpath,col[0],audio_url,video_url)
        # t = threading.Thread(target=download, args=(col[0],audio_url,video_url))
    except Exception as e:
        log.error(e)
        log.error(f"{col[0]}视频资源加载失败!")
    # 请求包含cid的页面
    temp = requests.get(f"https://api.bilibili.com/x/player/pagelist?bvid={col[3]}&jsonp=jsonp",
                        headers=headers).content.decode("utf-8")

    # 将cid抓取出来（如果不加[0]获取的将是一个列表）
    # 经过观察，列表内有且只有一个cid 所以通过索引的方式直接获取出来即可
    cid = re.findall('"cid":(.*?),', temp)[0]

    # 通过cid获取该视频的弹幕
    temp = requests.get(f"https://comment.bilibili.com/{cid}.xml", headers=headers).content.decode("utf-8")
    # 根据匹配模式，获取到的是弹幕出现时间、弹幕样式、字号、字体颜色、时间戳、弹幕池
    # 根据以上特征我们可以推测出UP主是一个什么样的性格、在粉丝眼中号召力如何、以及视频质量怎么样。
    temp = re.findall('<d p="(.*?),(.),(.*?),(.*?),(.*?),(.),(.*?),.*?">(.*?)<', temp)
    # 标题 ["弹幕出现时间","弹幕样式","字号","字体颜色","时间戳","弹幕池"]
    # 构造属于自己的数据格式
    ls = []
    for i in temp:
        t = {}
        t["弹幕出现时间"] = i[0]
        t["弹幕样式"] = i[1]
        t["字号"] = i[2]
        t["字体颜色"] = i[3]
        t["时间戳"] = i[4]
        t["弹幕池"] = i[5]
        t["发送者id"] = i[6]
        t["弹幕内容"] = i[7]
        if t["弹幕池"] == '0':
            ls.append(t)

    # 文件名中的非法字符替换为-
    fileName = re.sub('[\/:*?"<>|]', '-', col[0])  # 去掉非法字符
    fileName=fileName.replace('\\','')
    with open(f"{mpath}\\{fileName}.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, ["弹幕出现时间", "弹幕样式", "字号", "字体颜色", "时间戳", "弹幕池","发送者id", "弹幕内容"])
        # 写标头
        writer.writeheader()
        #  写内容
        writer.writerows(ls)
        # 直接将该列表存进数据库中
        saveMongo(ls)
    log.info(f"视频{col[0]}的弹幕爬取完毕...")


# 测试
if __name__ == "__main__":
    # 这两种链接的处理方式有点问题
    # https://space.bilibili.com/66607740?spm_id_from=333.999.0.0
    # https://space.bilibili.com/66607740/?spm_id_from=333.999.0.0
    # https://space.bilibili.com/2026561407?spm_id_from=333.337.0.0
    # https://space.bilibili.com/389860960?spm_id_from=333.337.0.0
    # url = input()
    # AllOpe(url)
    # 测试数据
    # uid 2026561407
    # cid 576484314
    # https://comment.bilibili.com/576484314.xml
    GetBarrage(("test","test","","BV1HS4y1c7Yk"))