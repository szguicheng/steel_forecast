import requests
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

url = 'https://www.corrdata.org.cn/pages/stationcorr.php?id=47#'
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
driver = webdriver.Chrome()
driver.get(url)
name = []  #所有材料牌号
final_T_data = []  #所有试验周期数据
final_num_data = []  #所有腐蚀失厚率数据
for material_id in range(1, 304):
    try:
        #找到响应的材料牌号并点击
        element = driver.find_element(
            By.XPATH,
            f'//ul[@class="side-menu"]/li[@data-material="{material_id}"]')
        element.click()
        time.sleep(0.3)

        #获取页面源码
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        #寻找腐蚀数据
        data = soup.find('div', id='data')
        tdatas = data.find_all('table')
        # print(tdatas)

        #每种材料数据清零
        eff_Ts = []  #每一材料种类试验周期的元素列表
        eff_nums = []  #每一材料种类腐蚀失厚率的元素列表
        T_datas = []  #每一材料种类试验周期的数据文本列表
        num_datas = []  #每一材料种类腐蚀失厚率的数据文本列表

        for tdata in tdatas:
            eff_Ts = tdata.find_all('th', text='试验周期')
            eff_nums = tdata.find_all('th', text='腐蚀失厚率')

            for eff_T in eff_Ts:  #找到试验周期对应的数据
                T_datas.append(eff_T.find_next_sibling('td').text)
            for eff_num in eff_nums:  #找到腐蚀失厚率对应的数据
                num_datas.append(eff_num.find_next_sibling('td').text)
        #将数据计入最终数据列表
        for T_data in T_datas:
            final_T_data.append(T_data)
        for num_data in num_datas:
            final_num_data.append(num_data)

        #获取材料牌号
        for T_data in T_datas:
            name.append(
                driver.find_element(
                    By.XPATH,
                    f'//ul[@class="side-menu"]/li[@data-material="{material_id}"]//strong'
                ).text)

        print(len(name), len(final_T_data), len(final_num_data),
              'material_id=', material_id)
        # print(name, final_T_data, final_num_data)

    except Exception as e:
        print(f"An error occurred: ", material_id, 'is error!')

# 创建 DataFrame
df = pd.DataFrame({
    '材料牌号': name,
    '腐蚀失厚率': final_num_data,
    '试验周期': final_T_data
})

# 保存为 Excel 文件
df.to_excel(
    f'/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据/steel_corr_Data.xlsx',
    index=False)

# print(len(name), len(final_T_data), len(final_num_data),material_id)
