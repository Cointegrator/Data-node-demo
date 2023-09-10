import pandas as pd
import re
import sys

df=pd.read_csv("indicators_now.csv")
df=df[['Coin name', 'indicators']]


onchains=[]
offchains=[]
for index, row in df.iterrows():
    indicators_list=[]
    coin_name = row['Coin name']
    indicators = row['indicators']
    #indicators = indicators.lower()
    
    print(f"Coin name: {coin_name}")
    #print("\n\n",indicators)
    # Use regular expression to extract lines starting with a number
    numbered_lines = re.findall(r'^\d+\..*$', indicators, re.MULTILINE)
    transformed_indicators = '\n'.join(numbered_lines)
    
    
    #print("\n\n", transformed_indicators)

    indicators_list = transformed_indicators.split('\n')

    # Create variables for onchain and offchain
    onchain = "\n".join(indicators_list[:5])
    offchain = "\n".join(indicators_list[5:])

    # Print the separated variables
    print("Onchain Indicators:")
    print(onchain)
    onchains.append(onchain)

    print("\nOffchain Indicators:")
    print(offchain)
    offchains.append(offchain)

    

    
df['onchain']=onchains
df['offchain']=offchains

print(df)

df=df[['Coin name', 'onchain', 'offchain','indicators']]

for index, row in df.iterrows():
    coin_name = row['Coin name']
    onchain = row['onchain']
    offchain=row['offchain']
    indicators = row['indicators']
    print(f"\n\n\n\n{coin_name}\n\n{onchain}\n\n{offchain}")


rows = []
for index, row in df.iterrows():
    coin_name = row['Coin name']
    onchain_indicators = row['onchain'].split('\n')
    offchain_indicators = row['offchain'].split('\n')
    
    for onchain, offchain in zip(onchain_indicators, offchain_indicators):
        onchain = onchain.split('. ')[1] 
        colon_index = onchain.index(":")
        # Extract the part of the string before the colon
        onchain = onchain[:colon_index]
        offchain = offchain.split('. ')[1]
        colon_index = offchain.index(":")
        # Extract the part of the string before the colon
        offchain = offchain[:colon_index]
        rows.append([coin_name, 'Onchain', onchain])
        rows.append([coin_name, 'Offchain', offchain])

# Creating a new DataFrame with the split rows
new_df = pd.DataFrame(rows, columns=['Coin name', 'Category', 'Indicator'])

new_df.to_csv('indicators_on_off_description_now.csv', index=False)  
print(new_df.head(10))

df=pd.read_csv("collected_description_now.csv")

df=df[['Coin name', 'Token','description_list']]
print(df.head(10))


# Merge based on 'Coin name' column
merged_df = pd.merge(new_df, df, on='Coin name', how='left')

merged_df = merged_df.rename(columns={'description_list': 'Coin Description'})


# Display the merged dataframe
print(merged_df)

merged_df.to_csv('indicators_on_off_description_now.csv', index=False)  