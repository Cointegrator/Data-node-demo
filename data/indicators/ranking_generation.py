


import pandas as pd

trend= pd.read_csv('trend_data_2023.csv',index_col='date')

columns_to_keep = [col for col in trend.columns if 'isPartial' not in col]
trend = trend[columns_to_keep]
print(trend.head())

price= pd.read_csv('crypto_data_11PM.csv',index_col=None)


print(price.head())

trend_transposed = trend.T.rename_axis('Coin name').reset_index()
print(trend_transposed.head())

# Rename the 'index' column to 'Coin name' and remove ' crypto'
trend_transposed['Coin name'] = trend_transposed['Coin name'].str.replace(' crypto', '')

# Merge the 'price' and 'trend' DataFrames on the 'Coin name' column
merged_df = pd.merge(price, trend_transposed, on='Coin name')

# Print the merged DataFrame
print(merged_df)

merged_df.to_csv('yearly_data.csv', index=False)

#on chain and offchain other indicators, percentage change 