import pandas as pd

# Read the contents of the files into pandas DataFrames
df_a = pd.read_excel('/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/异常值.xlsx')
df_b = pd.read_excel('/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据/腐蚀数据.xlsx')
# Remove rows from df_b where the index value matches the first column of df_a
df_c = df_b[~df_b.index.isin(df_a['异常index'])]

# Save the resulting DataFrame to a new Excel file
df_c.to_excel('/Users/guicheng/Documents/大学/本科学业/毕业设计/腐蚀数据处理/删除异常值后的腐蚀数据.xlsx',
              index=False)
