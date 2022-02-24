import csv
import os
import pandas as pd
import torch
import numpy as np

# TODO: add connections without flights, have all of their time series as 0s
# TODO: Change to weekly time steps
# TODO: add a "position" argument in the paths csv by averaging out position from both airports

airports = []
airport_connections = []
airport_dict = {}
airport_connections_dict = {}
airport_connection_number = 0
airports_number = 0
current_day = 1
days = 0
weeks = 0

for year in [2003, 2004, 2005, 2006, 2007, 2008]:

    print("YEAR: " + str(year))
    file = pd.read_csv("clean_2004_56_.csv")
    file_list = file.values.tolist()
    for i in range(len(file_list)):
        # if i % 10000 == 0:
        # print(i)
        if file_list[i][3] != current_day:
            current_day = file_list[i][3]
            days += 1
            if days % 7 == 0:
                days = 0
                weeks += 1
                print("week " + str(weeks))
            print(str(file_list[i][2]) + "/" + str(file_list[i][3]))
        if (file_list[i][6]) not in airports:
            airports.append(file_list[i][6])
            airports_number += 1
            airport_dict[file_list[i][6]] = airports_number

        if ([file_list[i][6], file_list[i][7]]) not in airport_connections:
            airport_connections.append([file_list[i][6], file_list[i][7]])
            airport_connection_number += 1

print(len(airport_connections))
print(airport_connection_number)

sorted_connections = sorted(airport_connections, key=lambda x: (x[0], x[1]))

matrix = np.zeros([weeks + 1, airport_connection_number])
print(matrix.shape)
current_day = 1
days = 0
weeks = 0

for year in [2003, 2004, 2005, 2006, 2007, 2008]:

    print("YEAR: " + str(year))
    file = pd.read_csv("clean_2004_56_.csv")
    file_list = file.values.tolist()
    for i in range(len(file_list)):
        # if i % 10000 == 0:
        # print(i)
        if file_list[i][3] != current_day:
            current_day = file_list[i][3]
            days += 1
            if days % 7 == 0:
                days = 0
                weeks += 1
                print("week " + str(weeks))
            print(str(file_list[i][2]) + "/" + str(file_list[i][3]))

        column = sorted_connections.index([file_list[i][6], file_list[i][7]]) - 1
        row = weeks
        matrix[row][column] += 1

pd.DataFrame(matrix).to_csv("matrix.csv", header=sorted_connections)
