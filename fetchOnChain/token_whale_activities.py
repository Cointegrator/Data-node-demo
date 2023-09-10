"""pip install flipside-sdk"""
from flipside import Flipside
import pandas as pd

"""Initialize Flipside with your API Key / API Url"""
flipside = Flipside("76894432-da55-49d0-95f0-c652265a59fd", "https://api-v2.flipsidecrypto.xyz")
sql = """with whale_addresses as ( select * from ethereum.core.ez_current_balances where contract_address = '0x701c244b988a513c945973defa05de933b23fe1d' and USD_VALUE_NOW >= 10000 ), transfers as ( select *, DATE_TRUNC('DAY', block_timestamp) as block_date from ethereum.core.ez_token_transfers where contract_address = '0x701c244b988a513c945973defa05de933b23fe1d' and block_timestamp >= '2023-08-10' and (from_address in (select USER_ADDRESS FROM whale_addresses) or to_address in (select USER_ADDRESS FROM whale_addresses)) ) select block_date, count(TX_HASH) as transfer_out_times from transfers group by block_date"""
"""Run the query against Flipside's query engine and await the results"""
query_result_set = flipside.query(sql)
df = pd.DataFrame(query_result_set.records)
df_sorted = df.sort_values(by='block_date', ascending=True)

# Convert the block_date to only include the date part
df['block_date'] = df['block_date'].str.split('T').str[0]
# Keep only the block_date and volumes columns
df = df[['block_date', 'transfer_out_times']]
# Display the modified DataFrame
df.to_csv('whales.csv')