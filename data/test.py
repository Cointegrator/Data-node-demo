import pandas as pd
from prophet import Prophet

df_default = pd.read_csv('test/8PM_data.csv', index_col=0)
mat_token = df_default.iloc[:,1:].transpose()
arr_columns = mat_token.columns[1:]

# Convert the string data to a DataFrame
df_default[['percentage']] = df_default['Percentage change'].str.rsplit(n=1, expand=True)
df_default['percentage'] = df_default['percentage'].str.rstrip('%').astype(float)
df_score1 = df_default['percentage']/100
df_score1.column = 'value'
df_score1 = df_score1.to_frame()

# Outperform
arr_result = []
for column in arr_columns:
    df_this = mat_token[column].to_frame()
    df_this.index.name = 'date'
    df_this.index = pd.to_datetime(df_this.index)
    df_this.index.name = 'date'
    df_daily = df_this.resample('D').sum()
    df_daily['ds'] = df_daily.index
    df_daily.columns = ['y', 'ds']
    m = Prophet()
    m.fit(df_daily)  # df is a pandas.DataFrame with 'y' and 'ds' columns
    future = m.make_future_dataframe(periods=1)
    score = m.predict(future)
    result = score['trend']
    score = (result.iloc[-1]- result.iloc[-2])/(result.iloc[-2] + 0.0001)
    arr_result.append([column, score])
df_score2 = pd.DataFrame(arr_result, columns=['Name', 'Value'])
df_score2.set_index('Name', inplace=True)

result = df_score1.add(df_score2, fill_value=0)
result.fillna(0, inplace=True)
result['total'] = result.sum(axis=1)
result['Rank'] = result['total'].rank(ascending=False, method='first')
df_sorted = result.sort_values(by='Rank')
df_sorted[['total','Rank']].to_csv('popularity.csv')

