import pandas as pd
df = pd.read_csv('dataset0.csv')
for i in range(1,1000):
	filename ='dataset'+i+'.csv'
	furniture_df = pd.read_csv(filename)
	df.append(furniture_df)


df.to_csv('dataset.csv')
