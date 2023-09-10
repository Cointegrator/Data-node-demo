from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import datetime
import numpy as np
import json

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
    df = pd.read_csv('./data/popularity.csv')
    return df.to_json(orient='records')



# get the asset table (the very left table on the left)
@app.route('/getIndicator', methods=['POST'])
def get_indicator():
    df = pd.read_csv('./data/indicators_on_off_description.csv')

    # append a percentage for random value
    df['Percentage'] = np.random.rand(len(df))
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
        ['Data Consistency', '20%'], 
        ['Reward', '5 Sei token'], 
        ['Prediction Capability', '12%'], 
    ]
  
    # Create the pandas DataFrame
    df = pd.DataFrame(data, columns=['name', 'value'])

    return df.to_json(orient='records')


# sanity check route
@app.route('/getTimeSeriesData', methods=['POST'])
def get_time_series_data():
    # Generate a range of dates in Unix milliseconds
    start_date = datetime.datetime(2023, 1, 1)
    end_date = datetime.datetime(2023, 1, 10)
    date_range = pd.date_range(start_date, end_date, freq='D')

    # Generate random numerical values
    num_values_1 = np.random.randint(1, 100, len(date_range))
    num_values_2 = np.random.randint(1, 100, len(date_range))

    # Create the DataFrame
    data_1 = {'Date': date_range.astype(int) // 10**6, 'Close': num_values_1}
    data_2 = {'Date': date_range.astype(int) // 10**6, 'Sentiment': num_values_2 }
    df_1 = pd.DataFrame(data_1)
    df_2 = pd.DataFrame(data_2)

    return {'price': json.loads(df_1.to_json(orient='records')), 'sentiment': json.loads(df_2.to_json(orient='records'))}



if __name__ == '__main__':
    app.run()
