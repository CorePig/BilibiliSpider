import matplotlib.pyplot as plt

# 用于正常显示中文
#plt.rcParams['font.family'] = ['sans-serif']#如果是windows系统请去掉这行注释
#plt.rcParams['font.sans-serif'] = ['SimHei']#如果是windows系统请去掉这
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

plt.figure(figsize=(8,6))#将画布设定为正方形，则绘制的饼图是正圆

values = [4.7,30.8,24.6,18.6,16,5.3]
label = ['西北','华东','华北','中南','西南','其他']
explode = [0.01,0.01,0.01,0.01,0.01,0.01]
patches,l_text,p_text = plt.pie(values,explode=explode,labels=label,autopct='%1.2f%%')#绘制饼图

for t in l_text:
    t.set_size(14)#图外的标注，如图中的华东等，可以修改字体大小
for l in p_text:
    l.set_size(15)#图内的标注，如图中的30.80%，可以修改字体大小

plt.suptitle('2019年中国大数据企业业务区域布局',fontsize=16,y=0.93)#绘制标题
plt.legend(bbox_to_anchor=(-0.04, 1),borderaxespad=0,frameon=False)#设置图例，这里bbox_to_anchor的作用是调整图例的位置，也可以通过设置loc='upper left'等选项设置位置
#plt.savefig('业务布局饼状图.png')#保存图片
plt.show()
