import time

from Search import *
from MsgFormat import *
import tkinter as tk
import tkinter.font as tkFont
from UserVerify import *
from Logs import *
# -------------------------------跳板区--------------------------------- #

# 开始爬虫（跳板）
def acction():
    global uid
    url = Url.get()
    uid, flag = AllOpe(url)
    if flag:
        tk.Label(window, text="收集完毕！", font=tipfont, fg="green").place(x=260, y=430, width=130, height=50)
        log.info(f"用户{uid}名下视频爬取完毕！")
    else:
        tk.Label(window, text="参数出错！", font=tipfont, fg="red").place(x=260, y=430, width=130, height=50)
        log.error("参数出错！")

# 开始数据分析（跳板）：
def analyse():
    # 验证用户数据是否存在，不存在的话提示系统出错

    # 判断id是否存在，不存在提示数据爬取。
    if not uid:
        tk.Label(window, text="未爬数据！", font=tipfont, fg="red").place(x=520, y=430, width=130, height=50)
        log.error("未爬取数据就开始数据分析！")
    else:
        window.destroy()
        MF=msgformat(uid)
        temp=MF.OneDayDfTime()
        temp.mainloop()


if __name__ == "__main__":
    # 进行身份验证
    UV = userverify()
    # https://space.bilibili.com/66607740?spm_id_from=333.999.0.0
    # https://space.bilibili.com/66607740/?spm_id_from=333.999.0.0
    # https://space.bilibili.com/2026561407?spm_id_from=333.337.0.0
    # https://space.bilibili.com/389860960?spm_id_from=333.337.0.0
    # 给出url
    # 根据url将弹幕爬到弹幕池中
    # 根据弹幕池分析博主视频质量
    # 根据某视频的弹幕判断视频中哪里最精彩
    # 画布
    if not UV.getflag():
        exit()

    while True:
        window = tk.Tk()
        window.title('B站弹幕爬取及分析。。。')
        window.geometry('900x600')

        # 字体样式
        h1 = tkFont.Font(family='Helvetica', size=44, weight=tkFont.BOLD)
        s1 = tkFont.Font(family='Helvetica', size=36, weight=tkFont.BOLD)
        s2 = tkFont.Font(family='Helvetica', size=20, weight=tkFont.BOLD)
        s3 = tkFont.Font(family='Helvetica', size=15)
        tipfont = tkFont.Font(family='Helvetica', size=17, weight=tkFont.BOLD)

        # 大标题
        s = 'B站弹幕爬取及分析'
        for i in range(9):
            tk.Label(window, text=s[i], font=h1).place(x=i * 100, y=100, width=100, height=100)

        # 读取框
        Url = tk.StringVar()
        # 获取到的用户id
        uid = ''

        tk.Button(window, text='开始爬取', font=s2, command=acction).place(x=130, y=430, width=120, height=50)
        tk.Button(window, text='数据分析', font=s2, command=analyse).place(x=400, y=430, width=120, height=50)
        tk.Button(window, text='退出系统', font=s2, command=quit).place(x=650, y=430, width=120, height=50)

        tk.Label(window, text="请输入URL:", font=s2).place(x=50, y=300, width=180, height=50)
        tk.Entry(window, textvariable=Url, font=s3).place(x=250, y=300, width=600, height=50)
        window.mainloop()






