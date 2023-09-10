from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import datetime
import plotly.express as px
import pandas as pd


df= pd.read_csv('trend_data_9PM.csv',index_col='date')

columns_to_keep = [col for col in df.columns if 'isPartial' not in col]
df = df[columns_to_keep]

# Create a figure
fig = px.line(df, x=df.index, y=df.columns, markers=True)

# Customize the layout
fig.update_layout(
    title='Trending coins Over Time',
    xaxis_title='Date',
    yaxis_title='Value',
    legend_title='Cryptocurrency',
)

# Show the plot
fig.show()

