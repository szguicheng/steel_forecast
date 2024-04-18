import requests
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import tqdm
from rich.progress import Progress, BarColumn, SpinnerColumn, TimeRemainingColumn, TimeElapsedColumn, TransferSpeedColumn
import requests
import openpyxl
from lxml import etree

# 国标定义区域
GBT13304 = [['C', 0, 2], ['Cr', 0.3, 0.5], ['Cu', 0.1, 0.5], ['Mn', 1, 1.4],
            ['Mo', 0.05, 0.1], ['Ni', 0.3, 0.5], ['Nb', 0.02, 0.06],
            ['Si', 0.5, 0.9], ['Ti', 0.05, 0.13], ['V', 0.04, 0.12],
            ['Zr', 0.05, 0.12]]
#定义区域
All_material_name = []  #所有材料牌号
standard_material_name = []  #符合国标的材料牌号
with Progress(
        "[progress.description]{task.description}({task.completed}/{task.total})",
        SpinnerColumn(finished_text="[green]✔"), BarColumn(),
        "[progress.percentage]{task.percentage:>3.2f}%", TimeElapsedColumn(),
        TimeRemainingColumn()) as progress:
    main_task = progress.add_task("[cyan]材料数据爬虫程序正在运行:", total=6)
    #获取X试验站的所有材料牌号
    minzi = '江津站'  #需要更改参数!!!!!!
    material_url = 'https://www.corrdata.org.cn/pages/stationcorr.php?id=33#'  #需要更改参数!!!!!!
    material_id = 0
    total1 = 1000  #需要更改参数!!!!!!
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    driver = webdriver.Chrome()
    driver.get(material_url)
    findall_material = progress.add_task("[green]正在获取该试验站的所有牌号材料",
                                         total=total1)
    for material_id in range(1, total1 + 1):
        try:
            #找到材料牌号对应标签
            All_material_name.append(
                driver.find_element(
                    By.XPATH,
                    f'//ul[@class="side-menu"]/li[@data-material="{material_id}"]//strong'
                ).text)
        except Exception as e:
            print(material_id, ':未找到该id材料')
        progress.update(findall_material, advance=1)
    print('材料种类总数量:', len(All_material_name))
    progress.update(main_task, advance=1)
    # 已找到所有材料牌号到All_material_name中
    # 进入材数库搜索单一材料的元素含量数据

    # All_material_name = ['16Mn', 'Q450NQR1', 'St12', 'Ste355', 'T2',
    #                      '1050A']  # 测试代码
    total2 = len(All_material_name)
    search_material_data = progress.add_task("[blue]正在匹配所有材料的元素含量数据",
                                             total=total2)
    for material_name in All_material_name:
        try:
            search_url = f'https://www.caishuku.com/material/index.php?keyword={material_name}&act=cal1'
            headers = {
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(search_url, headers=headers)
            print('<<<<<正在材料数据库中搜索', material_name, '的数据>>>>>')
            soup = BeautifulSoup(response.text, 'html.parser')
            location = soup.select_one(
                'div.layui-col-md9>div.layui-row:nth-of-type(4) a')
            if location is not None:
                element_url = 'https://www.caishuku.com' + location.get('href')
                print('--获取到', material_name, '的元素含量数据链接--')
            else:
                element_url = None
                print('--没有在材料数据库中找到', material_name, '的相应元素数据--\n')
                progress.update(search_material_data, advance=1)
            #已收集到材料数据的url到material_url中
            #下载单一材料的元素含量
            element_namelist = []
            element_min_valuelist = []
            element_max_valuelist = []
            if element_url is not None:
                element_response = requests.get(element_url, headers=headers)
            else:
                continue
            soup1 = BeautifulSoup(element_response.text, 'html.parser')
            try:
                element_table_source = soup1.find('legend',
                                                  text=re.compile('化学元素成分含量'))
            except Exception as table_error:
                print(material_name, '未找到元素含量数据表')
            element_table = element_table_source.find_parent().find_all('tr')
            #已找到元素含量数据[表]到element_table中
            #获取元素名称，最小值，最大值的[元素]到temp列表
            element_namelist_temp = [
                th for th in element_table[0].find_all('th')
            ]
            element_min_valuelist_temp = [
                td for td in element_table[1].find_all('td')
            ]
            element_max_vlauelist_temp = [
                td for td in element_table[2].find_all('td')
            ]
            #判断没有跨行情况就将数据文本计入正式列表
            for name_index in range(1, len(element_namelist_temp)):
                if element_min_valuelist_temp[name_index].get(
                        'rowspan') is None and element_max_vlauelist_temp[
                            name_index].get('rowspan') is None:
                    element_namelist.append(
                        element_namelist_temp[name_index].text.replace(
                            ' ', ''))
                    element_min_valuelist.append(
                        element_min_valuelist_temp[name_index].text.replace(
                            '-', '0'))
                    element_max_valuelist.append(
                        element_max_vlauelist_temp[name_index].text.replace(
                            '-', '0'))
            #如果数据符合国标则存入数据库
            material_flag = 0
            try:
                C_value_min = float(
                    element_min_valuelist[element_namelist.index('C')])
                C_value_max = float(
                    element_max_valuelist[element_namelist.index('C')])
                print('√√√', material_name, '有 C 元素的具体数据:', C_value_min,
                      C_value_max)

                C_flag = 0
                #判断条件
                if not ((C_value_min > GBT13304[0][2]) or
                        (C_value_max < GBT13304[0][1])):
                    C_flag = 1
                else:
                    C_flag = 0
                if C_flag == 1:
                    for element_data in GBT13304[1:]:
                        min_value = 0
                        max_value = 0
                        try:
                            min_value = float(
                                element_min_valuelist[element_namelist.index(
                                    element_data[0])])
                            max_value = float(
                                element_max_valuelist[element_namelist.index(
                                    element_data[0])])
                            print('√√√',
                                  material_name,
                                  '有',
                                  element_data[0],
                                  '元素的具体数据:',
                                  min_value,
                                  max_value,
                                  end=',')
                            #判断条件
                            element_flag = 0
                            if not ((min_value > element_data[2]) or
                                    (max_value < element_data[1])):
                                element_flag = 1
                                print(element_data[0], '符合国标')
                                break
                        except ValueError:
                            pass
            except ValueError:
                print('xxx', material_name, '没有 C 元素的具体数据')
            if element_flag == 1:
                material_flag = 1
            if material_flag == 1 and C_flag == 1:
                standard_material_name.append(material_name)
                print(material_name, '为低合金钢,已存入待爬取列表\n')
            else:
                print(material_name, '不是低合金钢,未存入数据库\n')
                #如果数据不符合国标则不存入
        except Exception as e:
            print(material_name, "爬取出现错误,以下是错误报告:", e, '\n')
        progress.update(search_material_data, advance=1)
    print('为低合金钢的材料牌号有:', standard_material_name)
    progress.update(main_task, advance=1)
    #在国家腐蚀网站上匹配数据库中的材料牌号并下载数据,在这一步进行材料牌号以及数据的数量匹配
    standard_material_id = []
    findall_material_id = progress.add_task("[red]正在获取该试验站的所有低合金钢牌号材料的id",
                                            total=len(standard_material_name))
    driver = webdriver.Chrome()
    driver.get(material_url)
    # driver.find_element(
    #                  By.XPATH,
    #                  f'//ul[@class="side-menu"]/li[@data-material="{material_id}"]//strong'
    #              ).text)
    for material_name in standard_material_name:
        strong_list = driver.find_elements(
            By.XPATH, '//ul[@class="side-menu"]/li//strong')
        for strong in strong_list:
            if strong.text == material_name:
                standard_material_id.append(
                    strong.find_element(By.XPATH, './..').find_element(
                        By.XPATH, './..').get_attribute('data-material'))
        progress.update(findall_material_id, advance=1)
    progress.update(main_task, advance=1)
    print('为低合金钢的材料牌号对应的id为:', standard_material_id)

    #在国家腐蚀网站上下载数据
    download_data = progress.add_task("[yellow]正在下载腐蚀数据",
                                      total=len(standard_material_id))

    final_T_data = []  #所有试验周期数据
    final_num_data = []  #所有腐蚀失厚率数据
    name = []  #所有材料牌号
    for material_id in standard_material_id:
        try:
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

            for T_data in T_datas:
                name.append(
                    driver.find_element(
                        By.XPATH,
                        f'//ul[@class="side-menu"]/li[@data-material="{material_id}"]//strong'
                    ).text)
            # print(len(name), len(final_T_data), len(final_num_data),
            #       'material_id=', material_id)
            # print(name, final_T_data, final_num_data)
        except Exception as e:
            print(material_id, "的腐蚀数据下载错误")
        progress.update(download_data, advance=1)
    progress.update(main_task, advance=1)

    #将数据存为excel
    # 计算最长的列的长度
    max_length = max(len(name), len(final_num_data), len(final_T_data))

    # 填充短的列
    name += [None] * (max_length - len(name))
    final_num_data += [None] * (max_length - len(final_num_data))
    final_T_data += [None] * (max_length - len(final_T_data))
    empty_list = [None] * max_length
    df = pd.DataFrame({
        '材料牌号': name,
        '腐蚀失厚率': final_num_data,
        '试验周期': final_T_data,
        'C_min': empty_list,
        'C_max': empty_list,
        'Si_min': empty_list,
        'Si_max': empty_list,
        'Mn_min': empty_list,
        'Mn_max': empty_list,
        'P_min': empty_list,
        'P_max': empty_list,
        'S_min': empty_list,
        'S_max': empty_list,
        'Cr_min': empty_list,
        'Cr_max': empty_list,
        'Ni_min': empty_list,
        'Ni_max': empty_list,
        'Cu_min': empty_list,
        'Cu_max': empty_list,
        'W_min': empty_list,
        'W_max': empty_list,
        'Mo_min': empty_list,
        'Mo_max': empty_list,
        'Sn_min': empty_list,
        'Sn_max': empty_list,
        'Sb_min': empty_list,
        'Sb_max': empty_list,
    })

    #加入材料元素数据
    download_element_data = progress.add_task(
        "[blue]正在下载元素数据", total=len(standard_material_name))
    start = 0
    stop = 0
    for material_name in standard_material_name:
        try:
            search_url = f'https://www.caishuku.com/material/index.php?keyword={material_name}&act=cal1'
            headers = {
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(search_url, headers=headers)
            print('<<<<<正在材料数据库中搜索', material_name, '的数据>>>>>')
            soup = BeautifulSoup(response.text, 'html.parser')
            location = soup.select_one(
                'div.layui-col-md9>div.layui-row:nth-of-type(4) a')
            if location is not None:
                element_url = 'https://www.caishuku.com' + location.get('href')
                print('--获取到', material_name, '的元素含量数据链接--')
            else:
                element_url = None
                print('--没有在材料数据库中找到', material_name, '的相应元素数据--\n')
                progress.update(search_material_data, advance=1)
            #已收集到材料数据的url到material_url中
            #下载单一材料的元素含量
            element_namelist = []
            element_min_valuelist = []
            element_max_valuelist = []
            if element_url is not None:
                element_response = requests.get(element_url, headers=headers)
            else:
                continue
            soup1 = BeautifulSoup(element_response.text, 'html.parser')
            try:
                element_table_source = soup1.find('legend',
                                                  text=re.compile('化学元素成分含量'))
            except Exception as table_error:
                print(material_name, '未找到元素含量数据表')
            element_table = element_table_source.find_parent().find_all('tr')
            #已找到元素含量数据[表]到element_table中
            #获取元素名称，最小值，最大值的[元素]到temp列表
            element_namelist_temp = [
                th for th in element_table[0].find_all('th')
            ]
            element_min_valuelist_temp = [
                td for td in element_table[1].find_all('td')
            ]
            element_max_vlauelist_temp = [
                td for td in element_table[2].find_all('td')
            ]
            #判断没有跨行情况就将数据文本计入正式列表
            for name_index in range(1, len(element_namelist_temp)):
                if element_min_valuelist_temp[name_index].get(
                        'rowspan') is None and element_max_vlauelist_temp[
                            name_index].get('rowspan') is None:
                    element_namelist.append(
                        element_namelist_temp[name_index].text.replace(
                            ' ', ''))
                    element_min_valuelist.append(
                        element_min_valuelist_temp[name_index].text.replace(
                            '-', '0'))
                    element_max_valuelist.append(
                        element_max_vlauelist_temp[name_index].text.replace(
                            '-', '0'))
        except Exception as e:
            print(material_name, "元素数据下载出现错误,以下是错误报告:", e, '\n')
        #开始处理数据位置
        stop = 0
        for same_material_name in name:  #处理数据长度
            if material_name == same_material_name:
                stop += 1
        for element in element_namelist:  #遍历所有元素
            try:
                if element == 'C':
                    for i in range(start, start + stop):
                        df.at[i, 'C_min'] = element_min_valuelist[
                            element_namelist.index(element)]
                        df.at[i, 'C_max'] = element_max_valuelist[
                            element_namelist.index(element)]
                if element == 'Si':
                    for i in range(start, start + stop):
                        df.at[i, 'Si_min'] = element_min_valuelist[
                            element_namelist.index(element)]
                        df.at[i, 'Si_max'] = element_max_valuelist[
                            element_namelist.index(element)]
                if element == 'Mn':
                    for i in range(start, start + stop):
                        df.at[i, 'Mn_min'] = element_min_valuelist[
                            element_namelist.index(element)]
                        df.at[i, 'Mn_max'] = element_max_valuelist[
                            element_namelist.index(element)]
                if element == 'P':
                    for i in range(start, start + stop):
                        df.at[i, 'P_min'] = element_min_valuelist[
                            element_namelist.index(element)]
                        df.at[i, 'P_max'] = element_max_valuelist[
                            element_namelist.index(element)]
                if element == 'S':
                    for i in range(start, start + stop):
                        df.at[i, 'S_min'] = element_min_valuelist[
                            element_namelist.index(element)]
                        df.at[i, 'S_max'] = element_max_valuelist[
                            element_namelist.index(element)]
                if element == 'Cr':
                    for i in range(start, start + stop):
                        df.at[i, 'Cr_min'] = element_min_valuelist[
                            element_namelist.index(element)]
                        df.at[i, 'Cr_max'] = element_max_valuelist[
                            element_namelist.index(element)]
                if element == 'Ni':
                    for i in range(start, start + stop):
                        df.at[i, 'Ni_min'] = element_min_valuelist[
                            element_namelist.index(element)]
                        df.at[i, 'Ni_max'] = element_max_valuelist[
                            element_namelist.index(element)]
                if element == 'Cu':
                    for i in range(start, start + stop):
                        df.at[i, 'Cu_min'] = element_min_valuelist[
                            element_namelist.index(element)]
                        df.at[i, 'Cu_max'] = element_max_valuelist[
                            element_namelist.index(element)]
                if element == 'W':
                    for i in range(start, start + stop):
                        df.at[i, 'W_min'] = element_min_valuelist[
                            element_namelist.index(element)]
                        df.at[i, 'W_max'] = element_max_valuelist[
                            element_namelist.index(element)]
                if element == 'Mo':
                    for i in range(start, start + stop):
                        df.at[i, 'Mo_min'] = element_min_valuelist[
                            element_namelist.index(element)]
                        df.at[i, 'Mo_max'] = element_max_valuelist[
                            element_namelist.index(element)]
                if element == 'Sn':
                    for i in range(start, start + stop):
                        df.at[i, 'Sn_min'] = element_min_valuelist[
                            element_namelist.index(element)]
                        df.at[i, 'Sn_max'] = element_max_valuelist[
                            element_namelist.index(element)]
                if element == 'Sb':
                    for i in range(start, start + stop):
                        df.at[i, 'Sb_min'] = element_min_valuelist[
                            element_namelist.index(element)]
                        df.at[i, 'Sb_max'] = element_max_valuelist[
                            element_namelist.index(element)]

            except Exception as e:
                print(element, '元素数据处理错误:', e)

        start += stop
        progress.update(download_element_data, advance=1)
    progress.update(main_task, advance=1)

    save_as_excel = progress.add_task("[green]正在保存数据为Excel文件", total=1)
    df.fillna(0, inplace=True)
    df.to_excel(f'/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据/{minzi}.xlsx',
                index=False)
    progress.update(save_as_excel, advance=1)
    progress.update(main_task, advance=1)
    print(f'{minzi}数据已保存为excel')
