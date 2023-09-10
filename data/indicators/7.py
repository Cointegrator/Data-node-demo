import pandas as pd
import re
import sys



df_pop=pd.read_csv("popularity.csv")
print(df_pop.head())


df_desc=pd.read_csv("collected_description_now.csv")

df_desc=df_desc[['Coin name', 'Token']]
df_desc.rename(columns={'Coin name': 'name'}, inplace=True)
#print(df_desc.head(10))

# Merge the dataframes on the 'name' column
merged_df = pd.merge(df_pop, df_desc, on='name')
print(merged_df.head())

merged_df.to_csv('popularity_final.csv', index=False)  