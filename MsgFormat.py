# 该模块主要的作用就是处理数据将数据可视化
# 着重分析UP主的视频适合什么时间段看并从所有弹幕中分析博主的性格
import copy
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
from Logs import *
# 防止matplotlib展示图像中文乱码
font = font_manager.FontProperties(fname=r"C:\\Windows\\Fonts\\msyh.ttc",size=12)

class msgformat:
    # 使用该类的时候必须先传进来一个uid进行初始化
    def __init__(self,uid):
        self.flag=True
        # 将传进来的uid设置为该类的一个属性
        self.uid=uid
        '''读取爬取到的数据'''
        # 先将所有的数据读取出来，然后将时间戳化为标准时间做一个弹幕时间图（24h那个时间段弹幕量大）
        mpath=sys.path[0]+"\\弹幕池\\"+self.uid+"\\"
        # ls是存储视频名称的列表
        self.ls=os.listdir(mpath)
        # lscount存储的是每一个视频对应的弹幕数量
        self.lscount=[]
        # mydata存储原始的数据，在其余地方进行数据分析的时候另外定义临时变量
        self.mydata=pd.DataFrame(columns=['弹幕出现时间','弹幕样式','字号','字体颜色','时间戳','弹幕池',"发送者id",'弹幕内容'])
        for i in self.ls:
            tempdata = pd.read_csv(mpath+i, engine="python",dtype = {'时间戳' : int})
            tempdata.columns=['弹幕出现时间','弹幕样式','字号','字体颜色','时间戳','弹幕池',"发送者id",'弹幕内容']
            self.lscount.append(len(tempdata))
            self.mydata=pd.concat([self.mydata,tempdata])
        '''画图用的属性区及介绍'''
        # self.ls 存储的是每一个视频的视频名称
        # self.lscount 存储的是每一个视频的弹幕数量
        # mtime是24个小时
        # timecount是每一个时间段的视频数量

        '''画布容器及主菜单'''
        self.root = tk.Tk()
        self.root.title("B站视频弹幕数据分析")
        self.root.geometry("1910x1080")
        self.tab_main=ttk.Notebook()
        self.tab_main.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.95)
    # set，get方法调节画布（扩展性）
    def setTabmain(self,frame):
        self.tab_main.add(frame)
    def getRootMenu(self):
        return self.root
    def getTabmain(self):
        return self.tab_main
    # 根据月份分析弹幕的数量
    def MounthMsg(self):
        tempdata=copy.deepcopy(self.mydata)
        tempdata['时间戳'] = self.mydata['时间戳'].apply(lambda x: datetime.utcfromtimestamp(x).strftime("%m"))
        # 数据的整体信息
        # print(self.mydata.info())
        # 用于存储不同月份弹幕的数量
        mouth = ["0" + str(i) if i < 10 else str(i) for i in range(1,13)]
        mouthcount = [0 for i in range(12)]
        # print(tempdata["时间戳"].value_counts())
        for i in range(12):
            # 统计某列某属性的数量
            try:
                mouthcount[i] = tempdata["时间戳"].value_counts()[mouth[i]]
            except Exception as e:
                mouthcount[i]=0
        # 再次处理月份名称（将0去掉月添上）
        mouth=[int(i) for i in mouth]
        mouth=[str(i)+"月" for i in mouth]
        # 以元组的形式返回分析后的数据
        return (mouth,mouthcount)
    # 分析发送弹幕最频繁的前15位用户
    def UserMax(self):
        tempdata=copy.deepcopy(self.mydata)
        t=tempdata["发送者id"].value_counts()
        # print(tempdata.info())
        # print(tempdata["发送者id"].value_counts())
        # 用户一共发送1条弹幕2条弹幕。。。。10条以上弹幕
        x=[1,2,3,4,5,6,7,8,9,10]
        y=[0]*10
        # 统计发送不同数目弹幕的用户
        for i in t:
            if i>=10:
                y[9]+=1
            else:
                y[i-1]+=1
        sums=sum(y)
        # 存放概率
        proY=[]
        for i in y:
            proY.append(i/sums)

        # 求个前缀和
        for i in range(1,len(proY)):
            proY[i]=proY[i-1]+proY[i]

        # 格式化一下小数位数
        proY=[float(format(i,".4f")) for i in proY]
        return (x,y,proY)




    # 第一个可视化页面负责展示一天不同时间段弹幕的数量
    def OneDayDfTime(self):
        # 进行列处理（将时间戳转换为时间只保留小时）
        tempdata=copy.deepcopy(self.mydata)
        tempdata['时间戳'] = self.mydata['时间戳'].apply(lambda x: datetime.utcfromtimestamp(x).strftime("%H"))
        # 数据的整体信息
        # print(mydata.info())
        # 用于存储不同时间段弹幕的数量
        mtime = ["0" + str(i) if i < 10 else str(i) for i in range(24)]
        timecount = [0 for i in range(24)]
        for i in range(24):
            # 统计某列某属性的数量
            timecount[i] = tempdata["时间戳"].value_counts()[mtime[i]]


        # 创建tkinter主界面


        '''第一个页面容器（24h不同时间段弹幕量分析）'''
        # 分析用户一般在什么时间段看视频（然后博主根据对应的用户群体可以推广指定商品）
        tx = np.array(mtime)
        ty = np.array(timecount)
        fig1 = plt.figure(figsize=[19, 10])
        plt.title("不同时间段弹幕数量折线图", fontproperties=font, fontdict={"color": "blue"})
        plt.ylabel("弹幕数量", fontproperties=font)
        plt.xlabel("时间段", fontproperties=font)
        # plt.yticks(range(len(tx)), , fontproperties=font)
        plt.xticks(range(len(tx)),tx)
        plt.plot(ty, 'r--o')
        # 网格线
        plt.grid()
        # 创建一个容器用于显示matplotlib的figer
        frame1 = tk.Frame(self.tab_main)
        frame1.place(x=300, y=10, width=1920, height=1080)
        # 将fig放入画布
        canvas = FigureCanvasTkAgg(fig1, master=frame1)
        canvas.draw()
        # 将画布放进窗口
        canvas.get_tk_widget().place(x=0, y=0)
        # 测试条形图
        self.tab_main.add(frame1,text="全天弹幕发布量分析")

        '''第二个页面（分析不同月份用户弹幕量，分析用户群体、上班族、学生族）'''
        Mouth=self.MounthMsg()# 返回的是元组(月份，月份弹幕量)
        colors = ["#00A4FF", "#4C5052", "#d71345", "#80752c",
                  "#b2d235", "#6950a1", "#45b97c", "#5f3c23",
                  "#840228", "#293047", "#f58220", "#225a1f"]
        frame2 = tk.Frame(self.tab_main)
        frame2.place(x=300, y=10, width=1920, height=1080)
        self.tab_main.add(frame2, text='博主月度弹幕数量统计')
        fig2 = plt.figure(figsize=(19, 10))  # 图像比例

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        explode = [0.01]*len(Mouth[0])
        # pctdistance = 1.1控制比例向外移动
        plt.pie(Mouth[1], explode=explode, labels=Mouth[0], autopct='%1.2f%%',pctdistance = 0.8,colors=colors)  # 绘制饼图

        plt.suptitle(f'用户{self.uid}不同月份视频弹幕量', fontsize=16, y=0.93)  # 绘制标题
        # 设置图例，这里bbox_to_anchor的作用是调整图例的位置，也可以通过设置loc='upper left'等选项设置位置
        plt.legend(bbox_to_anchor=(-0.5, 1), borderaxespad=0,frameon=False)
        canvas_spice = FigureCanvasTkAgg(fig2, frame2)
        canvas_spice.get_tk_widget().place(x=0,y=0)  # 放置位置

        '''第三个页面概率条形统计图'''
        userx,usery,userpro=self.UserMax()
        fig3 = plt.figure(figsize=(19, 10))  # 图像比例
        frame3 = tk.Frame(self.tab_main)
        frame3.place(x=300, y=10, width=1920, height=1080)
        # 测试条形图
        self.tab_main.add(frame3,text="用户弹幕数量统计")
        # 绘柱状图
        plt.bar(x=userx, height=usery, label='人数', color='#00A4FF', alpha=0.8)
        for a, b in zip(userx, usery):
            plt.annotate(b, xy=(a, b), xytext=(a-0.1, b + 20))
        # 在左侧显示图例
        plt.legend(loc="upper left")

        # 设置标题
        plt.title("累计弹幕条数统计")
        # 为两条坐标轴设置名称
        plt.xlabel("弹幕数量（条）")
        plt.ylabel("人数（人）")

        # 画折线图
        ax2 = plt.twinx()
        ax2.set_ylabel("比例")
        # 设置坐标轴范围
        ax2.set_ylim([0, 1.05]);
        plt.plot(userx, userpro, "r", marker='.', ms=5, linewidth='1', label="比例")
        # 显示数字
        for a, b in zip(userx, userpro):
            plt.annotate(b, xy=(a, b), xytext=(a-0.2, b + 0.01))
        # 在右侧显示图例
        plt.legend(loc="upper right")
        # 细化处理横坐标
        userx[len(userx)-1]="10条以上"
        userx.insert(0,0)
        plt.xticks(np.arange(len(userx)),userx)
        # 将fig放入画布
        canvas = FigureCanvasTkAgg(fig3, master=frame3)
        canvas.draw()
        # 将画布放进窗口
        canvas.get_tk_widget().place(x=0, y=0)



        # 调试用的
        self.root.mainloop()
        return self.root

if __name__=="__main__":
    test=msgformat('66607740')
    # test=msgformat('2026561407')
    test.OneDayDfTime()
    # test.MounthMsg()
    # test.UserMax()