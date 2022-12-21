# 该模块主要的作用就是处理数据将数据可视化
# 着重分析UP主的视频适合什么时间段看并从所有弹幕中分析博主的性格

import os
import sys
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import font_manager
import tkinter as tk
import numpy as np
from tkinter import *
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

font = font_manager.FontProperties(fname=r"C:\\Windows\\Fonts\\msyh.ttc", size=12)


def OneDayDfTime(uid):
    # 先将所有的数据读取出来，然后将时间戳化为标准时间做一个弹幕时间图（24h那个时间段弹幕量大）
    # 对所有弹幕进行分词处理，抽出排名前15的词
    mpath = sys.path[0] + "\\弹幕池\\" + uid + "\\"
    ls = os.listdir(mpath)
    lscount = []
    mydata = pd.DataFrame(columns=['弹幕出现时间', '弹幕样式', '字号', '字体颜色', '时间戳', '弹幕池', '弹幕内容'])
    for i in ls:
        tempdata = pd.read_csv(mpath + i, engine="python", dtype={'时间戳': int})
        tempdata.columns = ['弹幕出现时间', '弹幕样式', '字号', '字体颜色', '时间戳', '弹幕池', '弹幕内容']
        lscount.append(len(tempdata))
        mydata = pd.concat([mydata, tempdata])
    # 进行列处理（将时间戳转换为时间）
    mydata['时间戳'] = mydata['时间戳'].apply(lambda x: datetime.utcfromtimestamp(x).strftime("%H"))
    # 数据的整体信息
    # print(mydata.info())
    # 用于存储不同时间段弹幕的数量
    mtime = ["0" + str(i) if i < 10 else str(i) for i in range(24)]
    timecount = [0 for i in range(24)]

    for i in range(24):
        # 统计某列某属性的数量
        timecount[i] = mydata["时间戳"].value_counts()[mtime[i]]

    # 按时间段分析弹幕
    '''
    print(mtime)
    print(timecount)
    print(sum(timecount))
    '''

    # 分析视频质量
    '''
    print(ls)
    print(lscount)
    print(sum(lscount))
    '''
    # 弹幕出现的时间、弹幕不同时间段出现的次数、不同视频、不同视频弹幕的数量
    # return (mtime,timecount,ls,lscount)

    # 创建tkinter主界面
    root = tk.Tk()
    root.title("smart controller")
    root.geometry("1910x1080")
    tab_main = ttk.Notebook()
    tab_main.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.95)

    tx = np.array(mtime)
    ty = np.array(timecount)

    vx = np.array(ls)
    vy = np.array(lscount)

    # 画一个总的弹幕折线图
    fig1 = plt.figure(figsize=[19, 10])
    plt.title("不同时间段弹幕数量折线图", fontproperties=font, fontdict={"color": "blue"})
    plt.ylabel("弹幕数量", fontproperties=font)
    plt.xlabel("时间段", fontproperties=font)
    # plt.yticks(range(len(tx)), , fontproperties=font)
    plt.xticks(range(len(tx)), tx)
    plt.plot(ty, 'r--o')
    # 网格线
    plt.grid()
    # 创建一个容器用于显示matplotlib的figer

    # 第一个页面容器
    frame1 = tk.Frame(tab_main)
    frame1.place(x=300, y=10, width=1920, height=1080)
    # 将fig放入画布
    canvas = FigureCanvasTkAgg(fig1, master=frame1)
    canvas.draw()
    # 将画布放进窗口
    canvas.get_tk_widget().place(x=0, y=0)
    # 测试条形图
    tab_main.add(frame1, text="折线统计分析")

    # 第二个页面
    frame2 = Frame(tab_main)
    frame2.place(x=300, y=10, width=1920, height=1080)
    tab_main.add(frame2, text='第二页')
    fig = plt.figure(figsize=(7, 4), dpi=100)  # 图像比例
    f_plot = fig.add_subplot(111)  # 划分区域
    canvas_spice = FigureCanvasTkAgg(fig, frame2)
    canvas_spice.get_tk_widget().place(relx=0.3, rely=0.1)  # 放置位置

    root.mainloop()

    # 画饼状图看看他这些视频的弹幕比重（哪个视频更优质）
    '''
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    fig2=plt.figure(figsize=(20, 10))  # 将画布设定为正方形，则绘制的饼图是正圆

    explode = [0.01]*len(vx)
    patches, l_text, p_text = plt.pie(vy, explode=explode, labels=vx, autopct='%1.2f%%')  # 绘制饼图

    for t in l_text:
        t.set_size(14)  # 图外的标注，如图中的华东等，可以修改字体大小
    for l in p_text:
        l.set_size(15)  # 图内的标注，如图中的30.80%，可以修改字体大小

    plt.suptitle(f'用户{uid}各视频弹幕占总体比例', fontsize=16, y=0.93)  # 绘制标题
    plt.legend(bbox_to_anchor=(-0.04, 1), borderaxespad=0,
               frameon=False)  # 设置图例，这里bbox_to_anchor的作用是调整图例的位置，也可以通过设置loc='upper left'等选项设置位置
    # plt.savefig('业务布局饼状图.png')#保存图片
    plt.show()
    '''
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    # plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    #
    # fig2=plt.figure(figsize=(20, 10))  # 将画布设定为正方形，则绘制的饼图是正圆
    #
    # explode = [0.01]*len(vx)
    # pctdistance = 1.1控制比例向外移动
    # patches, l_text, p_text = plt.pie(vy, explode=explode, labels=vx, autopct='%1.2f%%',pctdistance = 1.1)  # 绘制饼图
    #
    # plt.suptitle(f'用户{uid}各视频弹幕占总体比例', fontsize=16, y=0.93)  # 绘制标题
    # plt.legend(bbox_to_anchor=(-0.04, 1), borderaxespad=0,frameon=False)
    # # 设置图例，这里bbox_to_anchor的作用是调整图例的位置，也可以通过设置loc='upper left'等选项设置位置
    # # plt.savefig('业务布局饼状图.png')#保存图片
    # plt.show()

    return root


if __name__ == "__main__":
    OneDayDfTime('66607740')
