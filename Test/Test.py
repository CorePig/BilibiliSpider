# 该模块主要的作用就是处理数据将数据可视化

import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib import font_manager
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

font = font_manager.FontProperties(fname=r"C:\\Windows\\Fonts\\msyh.ttc",size=10)
data=pd.read_csv(r"处理前的股票数据.csv",engine="python")
new_index=["序号"
    ,"代码"
    ,"名称"
    ,"价格"
    ,"涨跌幅"
    ,"涨跌额"
    ,"5分钟涨跌额"
    ,"今开"
    ,"昨收"
    ,"最高值"
    ,"最低值"
    ,"成交量"
    ,"成交额"
    ,"换手率"
    ,"量比"
    ,"委比"
    ,"振幅"
    ,"市盈率"
    ,"流通市值"
    ,"总市值"
    ,"每股收益"
    ,"净利润"
    ,"主营收"]
data.columns=new_index
print(data)
data=data[["代码","名称","价格","涨跌幅","涨跌额","最高值","最低值","成交额"]]
# 切片后剩余的列
data
# 查看是否存在空值
data.info()

# 处理data中成交额的文字（将他去掉）
# data["成交额"].str[0:-1]
tempvalue=[]
for temp in data["成交额"]:
    if temp[-1]=='万':
        tempvalue.append(str(float(temp[0:-1])*0.0001)[0:6])

temp1=data[data["成交额"].str[-1]=="亿"]
temp2=data[data["成交额"].str[-1]=="万"]
# 有些数据成交额为0
temp3=data[data["成交额"].str[0:]=="0"]
temp1["成交额"]=temp1["成交额"].str[0:-1]
temp2["成交额"]=tempvalue
# 拼接数据
data=pd.concat([temp1,temp2,temp3],axis=0)
print(data.info())
# 这里少100多行是正常的,因为爬取数据的时候每一页信息存进来的时候会多一行索引
# 一共有194行索引，将他去除了，所以现在有4662条数据
data
# 将该列类型进行转换,否则会根据ascll值进行排序
data[['成交额']]= data[['成交额']].values.astype(float)
# 按照成交量进行排序
data.sort_values("成交额",inplace=True,ascending=False)
data
import numpy as np
# 取出前15个数据
temp_data=data[0:15]
temp_data.sort_values('成交额',inplace=True,ascending=True)
temp_xy=temp_data[['名称','成交额']]
x=np.array(temp_xy['名称'])
y=np.array(temp_xy['成交额'])

color=['#F0F8AF',
'#FAEBD7',
 '#00FFFF',
'#7FFFD4',
'#F0AFFF',
'#F5F5DC',
'#FAE4C5',
'#0000A0',
'#FAABCD',
'#0F00FF',
'#8A2BE2',
'#A52A2A',
'#DEB887',
'#5F9EA0',
'#7FAF50']
fig1=plt.figure(figsize=[8,4])
plt.barh(range(15),y,color=color)
plt.title("股市成交额排名",fontproperties=font,fontdict={"color":"blue"})
plt.ylabel("公司名称",fontproperties=font)
plt.xlabel("交易额",fontproperties=font)
# plt.legend(prop=font)
plt.yticks(range(15),x,fontproperties=font)
plt.grid()
# plt.show()

data.to_csv("处理后的股票数据.csv",sep=',',index=False)



# 创建tkinter主界面
root = tk.Tk()
root.title("smart controller")
root.geometry("1920x1080")
# 创建一个容器用于显示matplotlib的fig
frame1 = tk.Frame(root)
frame1.place(x=0, y=30, width=800, height=600)
# 将fig放入画布
canvas = FigureCanvasTkAgg(fig1, master=frame1)
canvas.draw()
# 将画布放进窗口
canvas.get_tk_widget().place(x=0, y=0)

## 再画一个
fig1=plt.figure(figsize=[8,4])
plt.barh(range(15),y,color=color)
plt.title("股市成交额排名",fontproperties=font,fontdict={"color":"blue"})
plt.ylabel("公司名称",fontproperties=font)
plt.xlabel("交易额",fontproperties=font)
# plt.legend(prop=font)
plt.yticks(range(15),x,fontproperties=font)
plt.grid()
# plt.show()

data.to_csv("处理后的股票数据.csv",sep=',',index=False)



# 创建一个容器用于显示matplotlib的fig
frame1 = tk.Frame(root)
frame1.place(x=100, y=300, width=800, height=600)
# 将fig放入画布
canvas = FigureCanvasTkAgg(fig1, master=frame1)
canvas.draw()
# 将画布放进窗口
canvas.get_tk_widget().place(x=0, y=0)
root.mainloop()
