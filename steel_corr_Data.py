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
name = []
final_num_names = []
final_num_text = []
for material_id in range(1, 500):
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

        eff_nums = []
        num_names = []
        eff_nums_text = []
        for tdata in tdatas:

            nums = tdata.find_all('td')
            for num in nums:  #找到有效值
                if num.text != '':
                    eff_nums.append(num)

        for eff_num in eff_nums:  #将有效值text记录
            eff_nums_text.append(eff_num.text)

        for eff_num in eff_nums:  #找到有效值对应的数据
            num_names.append(eff_num.find_previous_sibling('th').text)

        #获取材料牌号
        flag = 0
        for index, num_name in enumerate(num_names):
            if num_name == '试验周期' or num_name == '腐蚀失厚率':
                final_num_names.append(num_name)
                final_num_text.append(eff_nums_text[index])
                flag += 1
                if (flag % 2) == 0 and flag != 0:
                    name.append(
                        driver.find_element(
                            By.XPATH,
                            f'//ul[@class="side-menu"]/li[@data-material="{material_id}"]//strong'
                        ).text)
        if len(name)*2 != len(final_num_text):
            print('error:', material_id, '金属种类数量', len(name), '~~~', '数据量',
                  len(final_num_text))

    except Exception as e:
        print(f"An error occurred: ", material_id, 'is error!')
#数据处理
list = [final_num_text[i:i + 2] for i in range(0, len(final_num_text), 2)]
# excel导出
# 将 list 分解为两个单独的列
col1 = [item[0] if len(item) > 1 else None for item in list]
col2 = [item[1] if len(item) > 1 else None for item in list]

# 创建 DataFrame
# df = pd.DataFrame({'材料牌号': name, '腐蚀失厚率': col2, '试验周期': col1})

# 保存为 Excel 文件
# df.to_excel(
#     f'/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据/steel_corr_Data.xlsx',
#     index=False)

print(len(name), len(col1), len(col2))
