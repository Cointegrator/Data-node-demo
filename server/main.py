from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/getAssetData', methods=['POST'])
def get_asset_data():
    data = [['AAPL', 10, 200, 10], ['TSLA', 15, 12, 13], ['GOOG', 14, 12, 15]]
  
    # Create the pandas DataFrame
    df = pd.DataFrame(data, columns=['asset_name', 'feature_0', 'feature_1', 'feature_2'])

    return df.to_json(orient='records')


# sanity check route
@app.route('/getTimeSeriesData', methods=['POST'])
def get_time_series_data():
    data = [['AAPL', 10, 200, 10], ['TSLA', 15, 12, 13], ['GOOG', 14, 12, 15]]
  
    # Create the pandas DataFrame
    df = pd.DataFrame(data, columns=['asset_name', 'feature_0', 'feature_1', 'feature_2'])

    return df.to_json(orient='records')




if __name__ == '__main__':
    app.run()
