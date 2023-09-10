from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import datetime
import plotly.express as px
import pandas as pd


pytrends = TrendReq(hl='en-US', tz=360)


# Replace 'crypto_data_8PM.csv' with the actual path to your CSV file
csv_file_path = 'coinranking_top_gainers_02.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Extract the values from the "Coin name" column into a list
coin_names = df['Coin name'].tolist()

#['Nest Protocol crypto', 'AGI Token crypto', 'Sperax crypto',
coin_names = [name + ' crypto' for name in coin_names]

print(coin_names)
kw_list = coin_names


#pytrends.build_payload(['BTC'], cat=0, timeframe='now 7-d', geo='US', gprop='')


#pd_data_frame =pytrends.interest_over_time()
#print(pd_data_frame)


# Initialize an empty DataFrame to store the results
pd_data_frame = pd.DataFrame()

chunk_size = 5
# Loop through chunks of kw_list
for i in range(0, len(kw_list), chunk_size):
    # Get a chunk of keywords
    chunk = kw_list[i:i + chunk_size]

    # Build payload for the current chunk
    #pytrends.build_payload(chunk, cat=cat, timeframe=timeframe, geo=geo, gprop=gprop)
    #pytrends.build_payload(chunk, cat=0, timeframe='all', geo='', gprop='')

    pytrends.build_payload(chunk, cat=0, timeframe='2023-01-01 2023-09-09', geo='', gprop='')
    #pytrends.build_payload(chunk, cat=0, timeframe='today 5-y', geo='', gprop='')

    # Get interest over time for the current chunk
    chunk_data = pytrends.interest_over_time()


    # Concatenate the chunk data to the main DataFrame
    if not pd_data_frame.empty:
        pd_data_frame = pd.concat([pd_data_frame, chunk_data], axis=1)
    else:
        pd_data_frame = chunk_data

# Print the final DataFrame
print(pd_data_frame)


pd_data_frame.to_csv('trend_data_2023.csv')

