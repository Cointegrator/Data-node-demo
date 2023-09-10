from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import datetime
import numpy as np
import json
import random

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/getAssetData', methods=['POST'])
def get_asset_data():
    data = [['AAPL', 10, 200], ['TSLA', 15, 12], ['GOOG', 14, 12]]
  
    # Create the pandas DataFrame
    df = pd.DataFrame(data, columns=['asset_name', 'feature_0', 'feature_1'])

    return df.to_json(orient='records')


# get the asset table (the very left table on the left)
@app.route('/getAsset', methods=['POST'])
def get_asset():
    df = pd.read_csv('./data/popularity_final.csv')
    return df.to_json(orient='records')



# get the asset table (the very left table on the left)
@app.route('/getIndicator', methods=['POST'])
def get_indicator():
    df = pd.read_csv('./data/indicators_on_off_description_now.csv')

    # append a percentage for random value
    df['Percentage'] = np.random.rand(len(df))

    print(df.head())
    return df.to_json(orient='records')


@app.route('/getUsers', methods=['POST'])
def get_user_data():
    data = [
        ['test1', 'John Sun1', 'john1@gmail.com'], 
        ['test2', 'John Sun2', 'john2@gmail.com'], 
        ['test2', 'John Sun3', 'john3@gmail.com'], 
    ]
    # Create the pandas DataFrame
    df = pd.DataFrame(data, columns=['user_name', 'name', 'email'])

    return df.to_json(orient='records')


@app.route('/getParameters', methods=['POST'])
def get_parameter_data():
    data = [
        ['Data Consistency', f'{random.randint(1, 100)}%'], 
        ['Reward', f'{random.randint(1, 10)} Sei token'], 
        ['Prediction Capability', f'{random.randint(1, 100)}%'], 
    ]
  
    # Create the pandas DataFrame
    df = pd.DataFrame(data, columns=['name', 'value'])

    return df.to_json(orient='records')


# sanity check route
@app.route('/getTimeSeriesData', methods=['POST'])
def get_time_series_data():
    js_input = json.loads(request.data)['params']
    asset_name = js_input['asset_name']
    indicator_name = js_input['indicator_name']

    df = pd.read_csv(f'./data/{asset_name}_{indicator_name}.csv')
    df['block_date'] = pd.to_datetime(df['block_date'])
    # Convert datetime column to UTC
    df['block_date'] = df['block_date'].dt.tz_localize('UTC')

    df['Date'] = df['block_date'].astype('int64') // 10**6 - 28800000

    
    # Sort the DataFrame by the 'unix_milliseconds' column
    df = df.sort_values(by='Date')

    print(df.tail(5))

    df = df.loc[:, ['Date', 'value']]

    return {
        'offchain': json.loads(df.to_json(orient='records'))
    }



if __name__ == '__main__':
    app.run()
