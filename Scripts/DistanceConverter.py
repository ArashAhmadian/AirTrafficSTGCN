import geopy.distance
import csv
import os
import pandas as pd
import torch
import numpy as np
import math
from geographiclib.geodesic import Geodesic

airport_coords = {}
airport_route_coords = {}
airport_route_coords_useful = {}
airport_route_useful_list = []
airport_route_useful_index = {}

airport_pairs = {}
airport_pairs_inverse = {}
airports_used = {}
airports_used_inverse = {}

airports_used_list = []
airport_pairs_used_list = []

airport_file = pd.read_csv('airports.csv', usecols=[4, 6, 7])
airport_file_list = airport_file.values.tolist()

for airport in airport_file_list:
    airport_coords[airport[0]] = [airport[1], airport[2]]

path_file = pd.read_csv("matrix.csv", header=None, low_memory=False)
path_file_list = path_file.values.tolist()
index = 0
for pair in path_file_list[0]:
    if str(pair) == "nan":
        continue

    airport_pairs[pair] = index
    index += 1
    airport_1 = pair[2:5]
    airport_2 = pair[9:12]

    if airport_1 not in airports_used_list:
        airports_used_list.append(airport_1)

    if airport_2 not in airports_used_list:
        airports_used_list.append(airport_2)

airport_pairs_inverse = {v: k for k, v in airport_pairs.items()}
airports_used_list.sort()
for i in range(len(airports_used_list)):
    airports_used[airports_used_list[i]] = i

airports_used_inverse = {v: k for k, v in airports_used.items()}

for airport_1 in airports_used_list:
    for airport_2 in airports_used_list:

        coords_1 = airport_coords.get(airport_1)
        coords_2 = airport_coords.get(airport_2)

        if airport_1 == "ILE" and airport_2 == "ILE":
            coords_1 = (31.07866667, -97.6866)
            coords_2 = (31.07866667, -97.6866)

        if airport_1 == "ILE":
            coords_1 = (31.07866667, -97.6866)

        if airport_2 == "ILE":
            coords_2 = (31.07866667, -97.6866)

        if coords_1 is not None and coords_1 != [0.0, 0.0]:
            coords_1 = tuple(coords_1)

        if coords_2 is not None and coords_2 != [0.0, 0.0]:
            coords_2 = tuple(coords_2)

        # print("COORDS 1:" + str(coords_1[0]) + str(coords_1[1]))
        # print("COORDS 2:" + str(coords_2[0]) + str(coords_2[1]))

        # Compute path from 1 to 2
        g = Geodesic.WGS84.Inverse(coords_1[0], coords_1[1], coords_2[0], coords_2[1])

        # Compute midpoint starting at 1
        h1 = Geodesic.WGS84.Direct(coords_1[0], coords_1[1], g['azi1'], g['s12'] / 2)
        #print(h1['lat2'], h1['lon2'])

        airport_route_coords[(airport_1, airport_2)] = (h1['lat2'], h1['lon2'])

        # if coords_1 is not None and coords_1 != [0.0, 0.0] and coords_2 is not None and coords_2 != [0.0, 0.0]:
        #    distance_matrix[airports_used[airport_1]][airports_used[airport_2]] = int(round(geopy.distance.distance(coords_1, coords_2).km))
        # else:
        #    distance_matrix[airports_used[airport_1]][airports_used[airport_2]] = None

index = 0
for key in airport_route_coords:
    pair = "[" + str(key)[1:-1] + "]"

    if pair in path_file_list[0]:
        airport_route_coords_useful[key] = airport_route_coords.get(key)
        airport_route_useful_list.append(key)
        airport_route_useful_index[key] = index
        index += 1

distance_matrix = np.zeros([len(airport_route_useful_list), len(airport_route_useful_list)])
i=0
for pair1 in airport_route_useful_list:
    print(i)
    i+=1
    for pair2 in airport_route_useful_list:

        coords_1 = airport_route_coords_useful.get(pair1)
        coords_2 = airport_route_coords_useful.get(pair2)

        if coords_1 is not None and coords_1 != [0.0, 0.0]:
            coords_1 = tuple(coords_1)

        if coords_2 is not None and coords_2 != [0.0, 0.0]:
            coords_2 = tuple(coords_2)



        if coords_1 is not None and coords_1 != [0.0, 0.0] and coords_2 is not None and coords_2 != [0.0, 0.0]:
            distance_matrix[airport_route_useful_index[pair1]][airport_route_useful_index[pair2]] = int(round(geopy.distance.distance(coords_1, coords_2).km))
        else:
            distance_matrix[airport_route_useful_index[pair1]][airport_route_useful_index[pair2]] = None

dataframe = pd.DataFrame(distance_matrix)

dataframe.to_csv("distances.csv")