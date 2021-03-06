#!/usr/bin/python
# -*- coding: utf-8 -*-
"""APS360_BaselineModel_Timeseries.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1znOyc5uYN688ChDujW8X8lYejHadSPoI

## APS360 Timeseries Baseline Model: Periodic Air Traffic Flow Forecasting Using Spatio-Temporal Convolutional Graph Neural Networks

Helen J Li

Group members: Arash Ahmadian Dehkordi, Callum McKelvie, Breno Pinho

NOTES TO RUN:
- you will need python3, pip3, matplotlib, pandas, and pmdarima installed in order to run this in your terminal.
- once the first plot shows, if you want to see the ARIMA model plotted next, you will have to close the window with the first plot.
"""

import  matplotlib.pyplot as plt
import pandas as pd
import subprocess
import sys

# read csv file for the first flight
abe_to_atl = pd.read_csv('../matrix.csv', header = 0, usecols = ["['ABE', 'ATL']"], nrows = 104)
df = abe_to_atl.plot()
df.get_legend().remove()
plt.title('ABE to ATL 2003 - 2004 Flights')
plt.xlabel('Week')
plt.ylabel('# Flights')
fig = plt.gcf()
fig.set_size_inches(16, 10)
plt.show()

# convert week numbers to date times so time series forecast model ARIMA can understand
df1 = pd.DataFrame({"Week": list(range(0,52)), "Year": 2003})
df1['Dates'] = pd.to_datetime(df1.Week.astype(str)+
                           df1.Year.astype(str).add('-1') ,format='%V%G-%u')
df2 = pd.DataFrame({"Week": list(range(0,52)), "Year": 2004})
df2['Dates'] = pd.to_datetime(df2.Week.astype(str)+
                           df2.Year.astype(str).add('-1') ,format='%V%G-%u')
frame = pd.concat([df1, df2])

# update csv object with new date time values
abe_to_atl.index = frame['Dates']
pd.set_option('display.max_rows', None)
abe_to_atl.head()

# eliminates time consuming parameter tuning processes and selects the best combination for you
from pmdarima.arima import auto_arima

model = auto_arima(abe_to_atl, start_p=1, start_q=1,
                           max_p=3, max_q=3, m=12,
                           start_P=0, seasonal=True,
                           d=1, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)

# split csv information into training and testing batches
train = abe_to_atl.loc['2002-12-23':'2004-09-06']
test = abe_to_atl.loc['2004-09-06':]

# train the model to the training data and predict 15 weeks in advance
model.fit(train)
forecast = model.predict(n_periods=15)
print(forecast)

#plot the predictions for validation set
forecast = pd.DataFrame(forecast,index = test.index,columns=['Prediction'])
plt.plot(abe_to_atl, label='Label Data')
plt.plot(forecast, label='Prediction')
plt.title('ABE/ATL 2003 - 2004 ARIMA Flight Prediction')
plt.xlabel('Time')
plt.ylabel('# Flights')
plt.legend()
fig = plt.gcf()
fig.set_size_inches(16, 10)
plt.show()

from datetime import datetime
import math
# calculate root mean squared error
sum = 0
average_percent_error = 0
for i in range(len(forecast)):
  date = df2['Dates'][i + 37].date().strftime("%Y-%m-%d")
  label = test["['ABE', 'ATL']"][date]
  predict = forecast["Prediction"][date]
  sum += (predict - label)**2
  average_percent_error += (abs(label - predict)/label)*100
print("Root mean squared error: ", math.sqrt(sum/len(forecast)))
print("Average percent error: ", average_percent_error/len(forecast))
