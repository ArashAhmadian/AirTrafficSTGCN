import csv
import os
import pandas as pd
import torch
import numpy as np

# WARNING: TAKES A LONG TIME TO RUN, HAS EVERY POSSIBLE CONNECTION BETWEEN AIRPORTS, EVEN ONES WITHOUT FLIGHTS
# ALSO: THIS FILE MIGHT BE USELESS. WHATEVER FILE USES THE MATRIX CAN JUST CHECK IF A SPECIFIC ENTRY EXISTS IN IT
# IF THE ENTRY DOES NOT EXIST, JUST ASSIGN A WEIGHT OF 0 TO THE TIME STEP IT IS TO BE USED FOR
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

for year in [2003]:

    file = pd.read_csv("clean_" + str(year) + "_56_.csv")
    file_list = file.values.tolist()
    for i in range(len(file_list)):
        #if i % 10000 == 0:
            #print(i)
        if file_list[i][3] != current_day:
            current_day = file_list[i][3]
            days += 1
            if days % 7 == 0:
                weeks += 1
            print(str(file_list[i][2]) + "/" + str(file_list[i][3]))
        if (file_list[i][6]) not in airports:
            airports.append(file_list[i][6])
            airports_number += 1
            airport_dict[file_list[i][6]] = airports_number
        if (file_list[i][7]) not in airports:
            airports.append(file_list[i][7])
            airports_number += 1
            airport_dict[file_list[i][7]] = airports_number

for airport in airports:
    for airport_2 in airports:
        airport_connections.append([airport, airport_2])
print(len(airport_connections))

sorted_connections = sorted(airport_connections, key=lambda x: (x[0], x[1]))

matrix = np.zeros([weeks+1, len(sorted_connections)])
print(matrix.shape)
current_day = 1
days = 0
weeks = 0

for year in [2003]:
    file = pd.read_csv("clean_" + str(year) + "_56_.csv")
    file_list = file.values.tolist()
    for i in range(len(file_list)):
        #if i % 10000 == 0:
            #print(i)
        if file_list[i][3] != current_day:
            current_day = file_list[i][3]
            days += 1
            if days % 7 == 0:
                weeks += 1
            print(days)

        column = sorted_connections.index([file_list[i][6], file_list[i][7]]) - 1
        row = weeks
        matrix[row][column] += 1


pd.DataFrame(matrix).to_csv("matrix.csv", header=sorted_connections)