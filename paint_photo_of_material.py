# 绘制材料的腐蚀速率图
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Specify the path to your Excel file
excel_file = '/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/第二次腐蚀数据获取/第二次腐蚀数据_outerr_human.xlsx'

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file)

config = {
    "font.family": "serif",  # 使用衬线体
    "font.serif": ["SimSun"],  # 全局默认使用衬线宋体
    "axes.unicode_minus": False,
    "mathtext.fontset": "stix",  # 设置 LaTeX 字体，stix 近似于 Times 字体
}
plt.rcParams.update(config)

ticklabels_style = {"fontname": "Times New Roman", "fontsize": 12}

# Read the first three columns of the DataFrame
place_list = df['试验地点'].tolist()
name_list = df['合金牌号'].tolist()
speed_list = df['腐蚀失厚率'].tolist()
time_list = df['试验周期'].tolist()
name = []
place = []
for i in name_list:
    if i not in name:
        name.append(i)

# Modify the place elements
# for i, p in enumerate(place_list):
#     if place_list[i] == '青岛':
#         place_list[i] = 'Qingdao'
#     elif place_list[i] == '万宁':
#         place_list[i] = 'Wanning'
#     elif place_list[i] == '琼海':
#         place_list[i] = 'Qionghai'
for i in place_list:
    if i not in place:
        place.append(i)
import matplotlib.pyplot as plt
import numpy as np

colors = [
    'red', 'green', 'blue', 'yellow', 'purple', 'cyan', 'magenta', 'black',
    'orange', 'pink'
]
markers = ['o', 's', 'D', 'v', '^', '<', '>', 'p', '*', 'h']

for num, i in enumerate(place):
    fig, axs = plt.subplots(figsize=(5, 5), dpi=400)
    fig.subplots_adjust(hspace=0.3, wspace=0.5)
    for j in name:
        x = []
        y = []
        for index, naming in enumerate(name_list):
            if naming == j and place_list[index] == i:
                x.append(time_list[index] / 12)
                y.append(speed_list[index])
        if name.index(j) <= len(colors):
            linestyle = '-'  # 使用虚线
        elif name.index(j) > len(colors) and name.index(j) <= 2 * len(colors):
            linestyle = '--'  # 使用实线
        elif name.index(j) > 2 * len(colors) and name.index(
                j) <= 3 * len(colors):
            linestyle = ':'
        sorted_indices = np.argsort(x)
        x_sorted = np.array(x)[sorted_indices]
        y_sorted = np.array(y)[sorted_indices]
        axs.plot(x_sorted,
                 y_sorted,
                 label=j,
                 color=colors[name.index(j) % len(colors)],
                 marker=markers[name.index(j) % len(markers)],
                 alpha=0.5,
                 markersize=3,
                 linewidth=0.6,
                 linestyle=linestyle)
        # axs.set_title(i)
        axs.set_xlabel('试验周期(年)')
        axs.set_ylabel('腐蚀失厚率' + r'$(\mu\text{m/a})$')
        # axs.legend(fontsize=6, frameon=False, bbox_to_anchor=(1.25, 1))
    plt.savefig(
        f'/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/第二次腐蚀数据获取/数据处理/outerr_human_{i}腐蚀数据图.png'
    )
    plt.clf()
# plt.suptitle('Corrosion Rate of different materials in different places',
#              fontsize=22)
# plt.savefig(
#     '/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/第二次腐蚀数据获取/数据处理/outerr_human_test腐蚀数据图.png'
# )
# plt.show()
# plt.clf()

from matplotlib.lines import Line2D

# 创建图例元素
legend_elements = [
    Line2D([0], [0],
           color=colors[name.index(j) % len(colors)],
           marker=markers[name.index(j) % len(markers)],
           label=j) for j in name
]

# 创建图例
fig, ax = plt.subplots(dpi=400)
ax.legend(handles=legend_elements, fontsize=12, frameon=False)

# 隐藏坐标轴
ax.axis('off')

# 保存图形
plt.savefig(
    '/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/第二次腐蚀数据获取/数据处理/legend.png',
    bbox_inches='tight',
    pad_inches=0)

# 清除图形
plt.clf()
