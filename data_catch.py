import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import tqdm
from rich.progress import Progress, BarColumn, SpinnerColumn, TimeRemainingColumn, TimeElapsedColumn, TransferSpeedColumn
import requests
import openpyxl
from lxml import etree

with Progress(
        "[progress.description]{task.description}({task.completed}/{task.total})",
        SpinnerColumn(finished_text="[green]✔"), BarColumn(),
        "[progress.percentage]{task.percentage:>3.2f}%", TimeElapsedColumn(),
        TimeRemainingColumn()) as progress:
    main_task = progress.add_task("[cyan]材料数据爬虫程序正在运行:", total=4)

    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 在此处输入需要爬取的材料名称
    material_name = [
        '00Cr19Ni10', '00Cr19Ni11', '06CuP(re)', '09CuP(re)', '09CuPCrNi',
        '09CuPCrNiA', '09CuPTiRe', '10Cr18Ni9Ti', '10CrCuSiV', '10CrMoAl',
        '14MnMoNbB', '15MnMoVN', '16Mn', '16MnQ', '20', '2Cr13', '2Cr14',
        '9CuPTiRe', 'A3', 'D36', 'Q235', 'Q450NQR1', 'St12', 'Ste355'
    ]
    # 在此处输入需要爬取的城市名称
    city_list = ['青岛', '琼海', '江津', '万宁']
    # 此处可以更改所需要的腐蚀数据字段(确保网站上的字段包含此处即可,无需精确匹配),如有更改,请一并更改下方代码的列标题df.columns以及数据类型转换
    corrotion_strings = ['合金牌号', '试验周期', '试验开始时间', '试验结束时间', '试验地点', '腐蚀失厚率']

    # 下载所有材料数据
    download_corrotion_data = progress.add_task("下载所有材料数据", total=100)
    corrotion_data = []
    i = 0
    for page in range(100):
        try:
            html = f'http://data.ecorr.org.cn/edata/01/0101/010101/01010101/index_{page}.html'
            response = requests.get(html, headers=headers)
            response.encoding = response.apparent_encoding
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            div = soup.find('div', class_='main_m fl')
            data_list = soup.find_all('div', class_='liebiao')
            for data in data_list:
                name = data.find('a').text
                eng_name = re.split(r'[\u4e00-\u9fff]', name)[0]
                place_name = re.search(r'[\u4e00-\u9fff]+', name).group()
                if eng_name in material_name:
                    if any(city in place_name for city in city_list):
                        corrotion_data.append([])
                        corrotion_data[i].append(eng_name)
                        url = data.find('a')['href']
                        url = 'http://data.ecorr.org.cn' + url
                        response = requests.get(url, headers=headers)
                        response.encoding = response.apparent_encoding
                        html = response.text
                        soup = BeautifulSoup(html, 'html.parser')
                        tr_list = soup.find_all('tr')
                        for _ in range(5):
                            corrotion_data[i].append('')
                        for index, string in enumerate(corrotion_strings[1:],
                                                       start=1):
                            for tr in tr_list:
                                if tr.find('div',
                                           string=re.compile(string)) != None:
                                    period_name = tr.find(
                                        'div', string=re.compile(string))
                                    period_name_parent = period_name.parent
                                    next_div = period_name_parent.find_next_sibling(
                                    ).find('div').text.replace('\r\n', '')
                                    corrotion_data[i][index] = next_div
                        print(corrotion_data[i])
                        i += 1
        except Exception as e:
            print(page, e)
        progress.update(download_corrotion_data, advance=1)
    # 保存数据
    df = pd.DataFrame(corrotion_data)
    df.columns = ['合金牌号', '试验周期', '试验开始时间', '试验结束时间', '试验地点', '腐蚀失厚率']
    try:
        df['合金牌号'] = df['合金牌号'].astype(str)
        df['试验周期'] = df['试验周期'].astype(int)
        df['试验开始时间'] = pd.to_datetime(df['试验开始时间'], format='%Y-%m-%d')
        df['试验结束时间'] = pd.to_datetime(df['试验结束时间'], format='%Y-%m-%d')
        df['试验地点'] = df['试验地点'].astype(str)
        df['腐蚀失厚率'] = df['腐蚀失厚率'].astype(float)
    except Exception as e:
        pass
    df.to_excel(
        '/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/第二次腐蚀数据获取/corrosion_temp_data.xlsx',
        index=False)
    progress.update(main_task, advance=1)

    #爬取所有天气数据
    download_weather_data = progress.add_task("下载所有天气数据", total=450)
    weather_data = []
    # 在此处可以修改所需爬取的天气数据字段(确保网站上的字段包含此处即可,无需精确匹配),如有更改,请一并更改下方代码的列标题df.columns以及数据类型转换
    weather_strings = [
        '试验地点', '试验时间', '平均温度', '平均相对湿度', '总辐射', '降水量', '降水时数', '平均风速',
        '瞬时法SO2', '瞬时法HCl', '连续法NO2'
    ]

    i = 0
    for x in [1, 8, 9]:
        for page in range(150):
            try:
                html = f'http://data.ecorr.org.cn/edata/01/0103/010301/0103010{x}/index_{page}.html'
                response = requests.get(html, headers=headers)
                response.encoding = response.apparent_encoding
                html2 = response.text
                soup2 = BeautifulSoup(html2, 'html.parser')
                div = soup2.find('div', class_='main_m fl')
                data_list = soup2.find_all('div', class_='liebiao')
                for data in data_list:
                    place = data.find('a').text
                    if any(city in place for city in city_list):
                        cityname = 0
                        for city in city_list:
                            if city in place:
                                cityname = city
                        weather_data.append([])
                        weather_data[i].append(cityname)
                        url = data.find('a')['href']
                        url = 'http://data.ecorr.org.cn' + url
                        response3 = requests.get(url, headers=headers)
                        response3.encoding = response3.apparent_encoding
                        html3 = response3.text
                        soup3 = BeautifulSoup(html3, 'html.parser')
                        tr_list = soup3.find_all('tr')
                        for _ in range(10):
                            weather_data[i].append('')
                        for index, string in enumerate(weather_strings[1:], start=1):
                            for tr in tr_list:
                                if tr.find('div', string=re.compile(string)) != None:
                                    period_name = tr.find('div', string=re.compile(string))
                                    period_name_parent = period_name.parent
                                    next_div = period_name_parent.find_next_sibling().find(
                                        'div').text.replace('\r\n', '')
                                    weather_data[i][index] = next_div

                        print(weather_data[i])
                        i += 1
            except Exception as e:
                print('page=', page, e)
            progress.update(download_weather_data, advance=1)
    # 保存数据
    df = pd.DataFrame(weather_data)
    df.columns = [
        '试验地点', '试验时间', '平均温度', '平均相对湿度', '总辐射', '降水量', '降水时数', '平均风速',
        '瞬时法SO2', '瞬时法HCl', '连续法NO2'
    ]
    try:
        df['试验地点'] = df['试验地点'].astype(str)
        df['试验时间'] = pd.to_datetime(df['试验时间'], format='%Y-%m-%d')
        df['平均温度'] = df['平均温度'].astype(float)
        df['平均相对湿度'] = df['平均相对湿度'].astype(float)
        df['总辐射'] = df['总辐射'].astype(float)
        df['降水量'] = df['降水量'].astype(float)
        df['降水时数'] = df['降水时数'].astype(float)
        df['平均风速'] = df['平均风速'].astype(float)
        df['瞬时法SO2'] = df['瞬时法SO2'].astype(float)
        df['瞬时法HCl'] = df['瞬时法HCl'].astype(float)
        df['连续法NO2'] = df['连续法NO2'].astype(float)
    except Exception as e:
        pass
    df.to_excel(
        '/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/第二次腐蚀数据获取/weather_temp_data.xlsx',
        index=False)
    progress.update(main_task, advance=1)

    #加入材料数据和天气数据列标题
    # 在此处可以修改所需计算的天气数据字段,请确保字段与上方下载的天气数据字段一致
    add_columns = progress.add_task("加入材料数据和天气数据列标题", total=1)
    data_string = [
        '平均温度', '平均相对湿度', '总辐射', '降水量', '降水时数', '平均风速', '瞬时法SO2', '瞬时法HCl',
        '连续法NO2'
    ]
    element_string = [
        'C_min', 'C_max', 'Si_min', 'Si_max', 'Mn_min', 'Mn_max', 'P_min',
        'P_max', 'S_min', 'S_max', 'Cr_min', 'Cr_max', 'Ni_min', 'Ni_max',
        'Cu_min', 'Cu_max', 'W_min', 'W_max', 'Mo_min', 'Mo_max', 'Sn_min',
        'Sn_max', 'Sb_min', 'Sb_max'
    ]

    corr_df = pd.read_excel(
        '/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/第二次腐蚀数据获取/corrosion_temp_data.xlsx'
    )
    corr_df.columns = ['合金牌号', '试验周期', '试验开始时间', '试验结束时间', '试验地点', '腐蚀失厚率'
                       ] + element_string + data_string
    corr_df.to_excel(
        '/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/第二次腐蚀数据获取/第二次腐蚀数据temp.xlsx'
    )
    progress.update(add_columns, advance=1)
    progress.update(main_task, advance=1)

    #根据腐蚀数据包含的试验时间段,计算该时间段内的天气数据
    corr_df = pd.read_excel(
        '/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/第二次腐蚀数据获取/第二次腐蚀数据temp.xlsx'
    )
    weather_df = pd.read_excel(
        '/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/第二次腐蚀数据获取/weather_temp_data.xlsx'
    )
    cal_weather_data = progress.add_task("计算腐蚀数据包含的天气数据",
                                         total=corr_df.shape[0])
    for index, row in corr_df.iterrows():
        start_time = pd.to_datetime(row['试验开始时间']).replace(day=1)
        end_time = pd.to_datetime(row['试验结束时间']).replace(day=1)
        mask = (weather_df['试验时间'].dt.to_period('M') >= start_time.to_period(
            'M')) & (weather_df['试验时间'].dt.to_period('M')
                     < end_time.to_period('M')) & (row['试验地点']
                                                   == weather_df['试验地点'])
        selected_data = weather_df[mask]
        for string in data_string:
            selected_data_nonzero = selected_data[(selected_data[string] != 0)  | (selected_data[string] != '') | (selected_data[string].notnull())]
            average_data = selected_data_nonzero[string].mean()
            corr_df.at[index, string] = average_data
        progress.update(cal_weather_data, advance=1)
    corr_df.to_excel(
        '/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/第二次腐蚀数据获取/第二次腐蚀数据.xlsx',
        index=False)
    progress.update(main_task, advance=1)
