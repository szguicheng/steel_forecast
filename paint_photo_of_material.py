# 绘制材料的腐蚀速率图
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Specify the path to your Excel file
excel_file = '/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/delcor_avg_human_腐蚀数据.xlsx'

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file)
# Read the first three columns of the DataFrame
name_list = df['合金牌号'].tolist()
speed_list = df['腐蚀失厚率'].tolist()
time_list = df['试验周期'].tolist()
name = []
for i in name_list:
    if i not in name:
        name.append(i)
for i in name:  #单独画每一个元素的图
    plt.figure
    indexs = [index for index, value in enumerate(name_list) if value == i]
    speed_value = [speed_list[index] for index in indexs]
    time_value = [time_list[index] for index in indexs]

    # Sort the values by time_value
    sorted_pairs = sorted(zip(time_value, speed_value))
    time_value, speed_value = zip(*sorted_pairs)

    plt.scatter(time_value, speed_value)
    plt.title(i)
    plt.xlabel('time/day')
    plt.ylabel('corrosion rate')
    # Fit a quadratic function to the scatter plot
    coefficients = np.polyfit(time_value, speed_value, 3)
    trendline = np.polyval(coefficients, time_value)

    # Plot the trendline
    plt.plot(time_value, trendline, color='red')
    plt.legend(['Scatter Data', 'Trendline'])
    # Save the plot as an image with the name of the variable i
    plt.savefig(
        f'/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/delcor_avg_human_腐蚀速率图/{i}.png'
    )
    plt.clf()
