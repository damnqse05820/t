import pandas as pd
from glob import glob

interesting_files = glob("*.csv") # it grabs all the csv files from the directory you mention here

df_list = []
for filename in sorted(interesting_files):
	df_list.append(pd.read_csv(filename,low_memory=False))
full_df = pd.concat(df_list)
del full_df['Unnamed: 0']
# save the final file in same/different directory:
full_df.to_csv("dataset.csv", index='false')


#from subprocess import call
#script="cat *.csv>merge.csv"
#call(script,Shell=True)

