import openai
import re

import pandas as pd


openai.api_key = "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"

def get_indicators(ticker, description):
    openai.api_key = "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"
    
    init_messages = [
    {"role": "system", "content": f"You are a trading expert. Your task is to find some 5 on-chain, and 5 off-chain indicators to predict price change of the crypto currency {ticker} {description} as a list"}
    ]

    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=init_messages,
        max_tokens=2000,  # Set a smaller maximum token limit
        n=1,
        stop=None,
        temperature=0,
    )

    message = completions.choices[0].message.content
    return message.strip()




df=pd.read_csv("collected_description_now.csv")
df=df[['Coin name','link','description_list']]
print(df.head(5))




results=[]
for index, row in df.iterrows():
    # Access the columns using row['column_name']
    name = row['Coin name']
    link = row['link']
    description_list=row['description_list']

    result=get_indicators(name, description_list)
    print(f"{name}\n{result}\n\n")
    
    results.append(result)
    print(f"{index} iteration done")
    


df['indicators']=results

# Save the DataFrame as a CSV file
df.to_csv('indicators_now.csv', index=False)  
