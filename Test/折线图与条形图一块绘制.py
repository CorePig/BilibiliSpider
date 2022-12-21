# -*- coding:utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文

# 构建数据
x = np.arange(1, 15)
y = [0.811, 0.88, 0.825, 0.76, 0.91, 0.95, 0.74, 0.99, 0.80, 0.72, 0.9, 0.81, 0.74, 0.87]
z = [37, 25, 17, 49, 27, 77, 34, 34, 34, 51, 39, 52, 47, 12]
u = [37, 31, 19, 57, 29, 86, 36, 37, 45, 64, 42, 57, 50, 24]

# 绘柱状图
plt.bar(x=x, height=z, label='实际', color='Coral', alpha=0.8)
# 在左侧显示图例
plt.legend(loc="upper left")

# 设置标题
plt.title("Detection results")
# 为两条坐标轴设置名称
plt.xlabel("Component number")
plt.ylabel("Number of seam")

# 画折线图
ax2 = plt.twinx()
ax2.set_ylabel("recall")
# 设置坐标轴范围
ax2.set_ylim([0.5, 1.05]);
plt.plot(x, y, "r", marker='.', label="Recall")
# 显示数字
for a, b in zip(x, y):
    plt.annotate(b,xy=(a,b),xytext=(a-0.5,b+0.01))
    # plt.text(a, b, b, ha='center', va='bottom', fontsize=8)
plt.xticks(np.arange(len(x)),x)
# 在右侧显示图例
plt.legend(loc="upper right")
plt.savefig("recall.jpg")

plt.show()
