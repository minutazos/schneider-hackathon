import pandas as pd
import numpy as np

df1 = pd.read_csv("train1.csv")
df2 = pd.read_csv("train2.csv", sep=';')
print(df2.shape[0])
print(df1.shape[0])
frames = [df1,df2]
df = pd.concat(frames)
print(df.shape[0])

names_list = df.columns.to_list()

aux = 0
for element in names_list:
    if df[element].isnull().values.any():
        aux = aux + 1
        print(df[element].isnull().values.any())
if aux > 0:
    print('existing nulls')
else:
    print('no existing nulls')