# 箱线图及异常值检测
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
from matplotlib.font_manager import FontProperties

font_path = FontProperties(fname='/System/Library/Fonts/STHeiti Light.ttc'
                           )  # 你需要替换为 'STKaiti' 字体在你的系统中的实际路径
# plt.figure(dpi=100)                                                          # 调整分辨率
df = pd.read_excel('/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据/腐蚀数据.xlsx')
ax = plt.gca()
# 设置图片大小
sns.boxplot(y=df['腐蚀失厚率'],
            width=0.66,
            boxprops=dict(facecolor=(0.39216, 0.58431, 0.92941, 0.7)))
sns.stripplot(y=df['腐蚀失厚率'], data=df, color="orangered", alpha=0.7, size=3)
# Swarn plot和stripplot比较类似，但Swarn plot的不同之处在于它不会重叠数据点
# sns.boxplot(y=df['Vcorr'],data=df)
# sns.swarmplot( y=df['Vcorr'], data=df, color="grey")
# sns.set_theme(style="whitegrid", font='STHeitiSC-Light')
# plt.rcParams['font.sans-serif'] = ['STHeitiSC-Light']
plt.rcParams["axes.linewidth"] = 20  # 设置边框粗细
plt.yticks(np.linspace(0, 800, 27), fontsize=10)  # 设置横坐标刻度、字体大小、坐标原点对齐
plt.ylabel("腐蚀失厚率(%)", fontsize=13, fontproperties=font_path)
# 设置横纵坐标的主次刻度
plt.tick_params(axis='y', which='major', labelsize=16, length=6, width=1.2)
plt.tick_params(axis='y', which='minor', length=4, width=1.1)
plt.tick_params(axis='x', which='major', length=6, width=1.2)
# 设置y轴主次刻度朝内
plt.tick_params(axis='x', direction='in')
plt.tick_params(axis='y', direction='in')
plt.tick_params(axis='y', direction='in', which='minor')
# 设置次刻度的数量
minor_locator = AutoMinorLocator(2)
ax.yaxis.set_minor_locator(minor_locator)
# 设置边框粗细
border_width = 1.6  # 指定边框的粗细
ax = plt.gca()  # 获取当前轴
plt.title('局部箱型图', fontsize=60, fontproperties=font_path)
plt.ylim(-25, 150)  #设置y轴范围
for pos in ['top', 'bottom', 'right', 'left']:
    ax.spines[pos].set_linewidth(border_width)
plt.tight_layout()
plt.savefig(
    '/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/局部箱型图ylim-25~150.png',
    dpi=600)
plt.show()
Q1 = df['腐蚀失厚率'].quantile(q=0.25)
Q3 = df['腐蚀失厚率'].quantile(q=0.75)
low_limit = Q1 - 1.5 * (Q3 - Q1)
up_limit = Q3 + 1.5 * (Q3 - Q1)
print('下限：', low_limit, '上限：', up_limit)
val = df['腐蚀失厚率'][(df['腐蚀失厚率'] > up_limit) | (df['腐蚀失厚率'] < low_limit)]
val.index.name = '异常index'
# val.to_excel('/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/异常值.xlsx',
#              index=True)
print('异常值如下：')
print(val)
