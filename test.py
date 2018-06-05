import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

ami = pd.read_excel('smartgrid.xlsx',sheet_name=0,header=8)
ami1 = pd.read_excel('smartgrid.xlsx',sheet_name=1,header=8)
ami2 = pd.read_excel('smartgrid.xlsx',sheet_name=2,header=8)


movies = pd.concat([ami, ami1, ami2])


print("Column headings:")
print(movies)

