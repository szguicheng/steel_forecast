# 随机森林特征重要性
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
from sklearn.preprocessing import StandardScaler
# 从CSV文件加载数据
df = pd.read_excel('/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/最终腐蚀数据.xlsx')
y = df['腐蚀失厚率']
X = df[[
    'C', 'Si', 'Mn', 'P', 'S', 'Cr', 'Ni', 'Cu', 'Mo', '平均温度', '平均相对湿度', '总辐照',
    '降水时数', '平均风速', '降雨量', '瞬时法SO2', '瞬时法HCL', '连续法NO2'
]]
# # 定义要尝试的树的数量范围
# n_estimators_range = [50, 100, 200, 300]
# # 创建一个空列表来存储OOB误差
# oob_errors = []
# # 创建一个空列表来存储特征重要性
# feature_importances = []
# # 循环尝试不同的树的数量
# for n_estimators in n_estimators_range:
# 创建随机森林回归模型
rf_regressor = RandomForestRegressor(n_estimators=150,
                                     oob_score=True,
                                     random_state=42)
# 标准化
scaler = StandardScaler()
X_normalized = scaler.fit_transform(X)
# 拟合模型
rf_regressor.fit(X_normalized, y)
# 计算OOB误差
oob_error = 1 - rf_regressor.oob_score_
# oob_error = mean_squared_error(y, rf_regressor.oob_prediction_)
print("OOB误差: {:.3f}".format(oob_error))
plt.rcParams['font.sans-serif'] = ['Artifakt Element']
# 获取当前轴
ax = plt.gca()
# 设置直线的起点和终点
# x_start, y_start = 0.43, -0.5
# x_end, y_end = 0.43, 7.5
# # 画直线
# ax.plot([x_start, x_end], [y_start, y_end], color='red', linestyle='--')
# # 添加双箭头
# arrow_params = dict(facecolor='red', edgecolor='red', arrowstyle='<->', lw=2)
# ax.annotate('', xy=(x_start, y_start), xytext=(x_end, y_end), arrowprops=arrow_params)
# # 调整字体
# ax.text(0.45, 3.5, 'Selected features', ha='center', va='center', color='black', rotation='270',
#         fontsize=19,fontfamily='Times New Roman')
# 获取特征重要性
feature_importance = rf_regressor.feature_importances_
# 创建特征名称列表
sub_map = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
SO2 = 'SO2'
NO2 = 'NO2'
feature_names = [
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
]
# 创建数据框以便于可视化
feature_importance_df = pd.DataFrame({
    'Features': feature_names,
    'Feature importances': feature_importance
})
# 对特征重要性进行排序
feature_importance_df = feature_importance_df.sort_values(
    by='Feature importances', ascending=False)
# 可视化特征重要性排序
# plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['Features'],
         feature_importance_df['Feature importances'])
plt.xlabel('Feature importances', fontsize=14)
# 添加水平虚线
# ax.axhline(y=7.5, color='red', linestyle='--', linewidth=2.1)
# 设置横纵坐标的主次刻度
plt.tick_params(axis='both', which='major', labelsize=12, length=6, width=1.3)
plt.tick_params(axis='x', which='minor', length=4, width=1.1)
# 设置横坐标刻度、字体大小、坐标原点对齐
plt.xticks(np.linspace(0, 0.5, 6), fontsize=14)
# 设置次刻度的数量
minor_locator = AutoMinorLocator(2)
ax.xaxis.set_minor_locator(minor_locator)
# 设置边框粗细
border_width = 1.6  # 指定边框的粗细
ax = plt.gca()  # 获取当前轴
for pos in ['top', 'bottom', 'right', 'left']:
    ax.spines[pos].set_linewidth(border_width)
# 逆序显示特征
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/特征重要性排序.png',
            dpi=600)
plt.show()
