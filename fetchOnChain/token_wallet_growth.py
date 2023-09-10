"""pip install flipside-sdk"""
from flipside import Flipside
import pandas as pd

mapping = {
'OpenANX':  '0x701c244b988a513c945973defa05de933b23fe1d',
'TOMI': '0x4385328cc4d643ca98dfea734360c0f596c83449',
'DREP':  '0x3ab6ed69ef663bd986ee59205ccad8a20f98b4c2',
'MIR':  '0x09a3ecafa817268f77be1283176b946c4ff2e608',
'BabyDoge':  '0xac57de9c1a09fec648e93eb98875b212db0d460b'
}


for coin in mapping:
    print(coin)
    """Initialize Flipside with your API Key / API Url"""
    flipside = Flipside("76894432-da55-49d0-95f0-c652265a59fd", "https://api-v2.flipsidecrypto.xyz")
    sql = """with transfers as ( select * from ethereum.core.ez_token_transfers where contract_address = '{}'  and block_timestamp >= '2023-08-10' ), first_txn as ( SELECT to_address, min(block_timestamp) as first_received FROM transfers GROUP BY to_address ), new_users as ( SELECT date_trunc('DAY', first_received) as block_date, count(DISTINCT to_address) as n_new_recipient from first_txn GROUP by 1 ) SELECT * FROM new_users""".format(mapping[coin])
    """Run the query against Flipside's query engine and await the results"""
    query_result_set = flipside.query(sql)
    df = pd.DataFrame(query_result_set.records)
    df_sorted = df.sort_values(by='block_date', ascending=True)

    # Convert the block_date to only include the date part
    df['block_date'] = df['block_date'].str.split('T').str[0]
    # Keep only the block_date and volumes columns
    df = df[['block_date', 'n_new_recipient']]
    # Display the modified DataFrame
    df.to_csv(coin + '_growth.csv')