# 归一化和相关性分析
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

df = pd.read_excel('/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/最终腐蚀数据.xlsx')
# 提取特征和目标变量
X = df[[
    'C', 'Si', 'Mn', 'P', 'S', 'Cr', 'Ni', 'Cu', 'Mo', '平均温度', '平均相对湿度', '总辐照',
    '降水时数', '平均风速', '降雨量', '瞬时法SO2', '瞬时法HCL', '连续法NO2'
]]
y = df['腐蚀失厚率']
# 使用 Min-Max 归一化将特征缩放到 [0, 1] 范围内
scaler = StandardScaler()
X_normalized = scaler.fit_transform(X)
sub_map = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
SO2 = 'SO2'
NO2 = 'NO2'
# plt.ylabel('{} Concentration'.format(SO2.translate(sub_map)), fontsize=14)
normalized_data = pd.DataFrame(X_normalized,
                               columns=[
                                   'C',
                                   'Si',
                                   'Mn',
                                   'P',
                                   'S',
                                   'Cr',
                                   'Ni',
                                   'Cu',
                                   'Mo',
                                   'Avg Temp',
                                   'Avg RH',
                                   'Total Radiation',
                                   'Precipitation Hours',
                                   'Avg Wind Speed',
                                   'Rainfall',
                                   SO2.translate(sub_map),
                                   'Cl-',
                                   NO2.translate(sub_map),
                               ])
# 计算相关系数矩阵
method = 'pearson'  # 'spearman'可以换成 'pearson'或 'kendall'
correlation_matrix = normalized_data.corr(
    method=method)  # 'spearman'可以换成 'pearson'或 'kendall'
# 打印相关系数矩阵
# print("特征之间的相关性：")
# print(correlation_matrix)
# 可视化相关性矩阵
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(9, 7))
# # 设置不使用其默认自带的colorbar
# h = sns.heatmap(correlation_matrix,
#                 annot=True,
#                 cmap='coolwarm',
#                 vmin=-1,
#                 vmax=1,
#                 linewidths=0.8,
#                 cbar=False,
#                 annot_kws={"fontsize": 15})
# # 显示colorbar
# cb = h.figure.colorbar(h.collections[0])
# # 设置colorbar刻度字体大小
# cb.ax.tick_params(labelsize=15)
plt.title(
    f"Normalized Correlation Matrix With Element Data({method.capitalize()} Method)",
    fontsize=14,
    pad=9)
# 创建相关性矩阵热图
heatmap = sns.heatmap(correlation_matrix,
                      annot=True,
                      cmap='coolwarm',
                      vmin=-1,
                      vmax=1,
                      linewidths=0.8,
                      annot_kws={"fontsize": 6})
# 获取颜色条对象
cbar = heatmap.collections[0].colorbar
# 设置颜色条刻度值的字体大小
cbar.ax.tick_params(labelsize=16)  # 设置刻度值的大小为16
plt.rcParams['font.sans-serif'] = ['Artifakt Element']
plt.rcParams['axes.unicode_minus'] = True
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
plt.savefig(
    f'/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/相关性分析热图/带有元素信息的相关性分析({method.capitalize()}方法).jpg',
    dpi=600)
# plt.show()
