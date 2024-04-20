# 绘制材料的腐蚀速率图
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Specify the path to your Excel file
excel_file = '/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/delcor_avg_human_腐蚀数据.xlsx'

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file)
# Read the first three columns of the DataFrame
place_list = df['实验地点'].tolist()
name_list = df['合金牌号'].tolist()
speed_list = df['腐蚀失厚率'].tolist()
time_list = df['试验周期'].tolist()
name = []
place = []
for i in name_list:
    if i not in name:
        name.append(i)

# Modify the place elements
for i, p in enumerate(place_list):
    if place_list[i] == '青岛':
        place_list[i] = 'Qingdao'
    elif place_list[i] == '北京':
        place_list[i] = 'Beijing'
    elif place_list[i] == '琼海':
        place_list[i] = 'Qionghai'
    elif place_list[i] == '广州':
        place_list[i] = 'Guangzhou'
for i in place_list:
    if i not in place:
        place.append(i)
import matplotlib.pyplot as plt
import numpy as np

# 假设你已经有了以下的列表：
# place: 包含所有实验站的列表
# name: 包含所有材料的列表
# name_list: 包含每个数据点对应的材料的列表
# time_list: 包含每个数据点的腐蚀时间的列表
# speed_list: 包含每个数据点的腐蚀速率的列表

colors = [
    'red', 'green', 'blue', 'yellow', 'purple', 'cyan', 'magenta', 'black',
    'orange', 'pink'
]
markers = ['o', 's', 'D', 'v', '^', '<', '>', 'p', '*', 'h']

fig, axs = plt.subplots(2, 2, figsize=(10, 10), dpi=600)
fig.subplots_adjust(hspace=0.3, wspace=0.5)
axs = axs.flatten()
for num, i in enumerate(place):
    for j in name:
        x = []
        y = []
        for index, naming in enumerate(name_list):
            if naming == j and place_list[index] == i:
                x.append(time_list[index])
                y.append(speed_list[index])
        if name.index(j) <= len(colors):
            linestyle = '-'  # 使用虚线
        elif name.index(j) > len(colors) and name.index(j) <= 2 * len(colors):
            linestyle = '--'  # 使用实线
        elif name.index(j) > 2 * len(colors) and name.index(
                j) <= 3 * len(colors):
            linestyle = ':'
        axs[num].plot(x,
                      y,
                      label=j,
                      color=colors[name.index(j) % len(colors)],
                      marker=markers[name.index(j) % len(markers)],
                      alpha=0.5,
                      markersize=3,
                      linewidth=0.4,
                      linestyle=linestyle)
        axs[num].set_title(i)
        axs[num].set_xlabel('Time/day')
        axs[num].set_ylabel('Corrosion rate')
        axs[num].legend(fontsize=6, frameon=False, bbox_to_anchor=(1, 1))
        axs[num].grid()
plt.suptitle('Corrosion rate of different materials in different places',
             fontsize=22)
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.savefig('/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/腐蚀数据图.png')
# plt.show()
plt.clf()
