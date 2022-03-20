import geopy.distance
import csv
import os
import pandas as pd
import torch
import numpy as np

airport_coords = {}

airport_pairs = {}
airport_pairs_inverse = {}
airports_used = {}
airports_used_inverse = {}

airports_used_list = []

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

distance_matrix = np.zeros([len(airports_used_list), len(airports_used_list)])


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

        if coords_1 is not None and coords_1 != [0.0, 0.0] and coords_2 is not None and coords_2 != [0.0, 0.0]:
            distance_matrix[airports_used[airport_1]][airports_used[airport_2]] = int(round(geopy.distance.distance(coords_1, coords_2).km))
        else:
            distance_matrix[airports_used[airport_1]][airports_used[airport_2]] = None


dataframe = pd.DataFrame(distance_matrix)

dataframe.to_csv("distances.csv")