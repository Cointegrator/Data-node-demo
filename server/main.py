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
