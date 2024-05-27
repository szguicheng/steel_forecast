import pandas as pd

df = pd.read_excel(
    '/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/第二次腐蚀数据获取/第二次腐蚀数据_outerr_human.xlsx'
)
df.insert(df.columns.get_loc('Cmax') + 1, 'C', ((df['Cmin'] + df['Cmax']) / 2))
df.insert(
    df.columns.get_loc('Simax') + 1, 'Si', ((df['Simin'] + df['Simax']) / 2))
df.insert(
    df.columns.get_loc('Mnmax') + 1, 'Mn', ((df['Mnmin'] + df['Mnmax']) / 2))
df.insert(df.columns.get_loc('Pmax') + 1, 'P', ((df['Pmin'] + df['Pmax']) / 2))
df.insert(df.columns.get_loc('Smax') + 1, 'S', ((df['Smin'] + df['Smax']) / 2))
df.insert(
    df.columns.get_loc('Crmax') + 1, 'Cr', ((df['Crmin'] + df['Crmax']) / 2))
df.insert(
    df.columns.get_loc('Nimax') + 1, 'Ni', ((df['Nimin'] + df['Nimax']) / 2))
df.insert(
    df.columns.get_loc('Cumin') + 1, 'Cu', ((df['Cumin'] + df['Cumax']) / 2))
df.insert(df.columns.get_loc('Wmax') + 1, 'W', ((df['Wmin'] + df['Wmax']) / 2))
df.insert(
    df.columns.get_loc('Momax') + 1, 'Mo', ((df['Momin'] + df['Momax']) / 2))
df.insert(
    df.columns.get_loc('Snmax') + 1, 'Sn', ((df['Snmin'] + df['Snmax']) / 2))
df.insert(
    df.columns.get_loc('Sbmax') + 1, 'Sb', ((df['Sbmin'] + df['Sbmax']) / 2))

df.to_excel(
    '/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/第二次腐蚀数据获取/第二次腐蚀数据_outerr_human1.xlsx',
    index=False)
