import pandas as pd

df1 = pd.read_csv("companies.csv", header=0, usecols=['name', 'homepage_url', 'category_list', 'country_code'])
print(list(df1[:5]['homepage_url']))
#df1[:5].to_csv('5companies.csv', header=False)