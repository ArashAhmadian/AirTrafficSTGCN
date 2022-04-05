import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
import numpy as np

def findAirportIndex(airportName, airportNameReader):

    for row in zip(airportNameReader['Airport'], airportNameReader['Name']):

        if row[1] == (" " + airportName):
            return row[0]

def RGBToHex(r, g, b):

  return "#%02X%02X%02X" % (r, g, b)

def map(x, inMin, inMax, outMin, outMax):

    return int((x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin)

def plotEdge(firstCoordinate, secondCoordinate, edgeTraffic, minTraffic, maxTraffic):

    colourOffset = map(edgeTraffic, minTraffic, maxTraffic, 0, 255)

    colour = RGBToHex(255 , 255 - colourOffset, 0)

    xValues = [firstCoordinate[0], secondCoordinate[0]]
    yValues = [firstCoordinate[1], secondCoordinate[1]]

    plt.plot(xValues, yValues, colour, linestyle="-")

#a = np.load("Files/testset_predictions_all_samples.npy")
#pd.DataFrame(a[:,0,:]).to_csv('Files/RoutePrediction1.csv')
#pd.DataFrame(a[:,1,:]).to_csv('Files/RoutePrediction2.csv')
#pd.DataFrame(a[:,2,:]).to_csv('Files/RoutePrediction3.csv')
#pd.DataFrame(a[:,3,:]).to_csv('Files/RoutePrediction4.csv')
#pd.DataFrame(a[:,4,:]).to_csv('Files/RoutePrediction5.csv')

#b = np.load("Files/testset_predictions_gtruths_all_samples.npy")
#pd.DataFrame(b[:,0,:]).to_csv('Files/RouteActual1.csv')
#pd.DataFrame(b[:,1,:]).to_csv('Files/RouteActual2.csv')
#pd.DataFrame(b[:,2,:]).to_csv('Files/RouteActual3.csv')
#pd.DataFrame(b[:,3,:]).to_csv('Files/RouteActual4.csv')
#pd.DataFrame(b[:,4,:]).to_csv('Files/RouteActual5.csv')
#
# c = np.load("Files/testset_MAPE_mean.npy")
# pd.DataFrame(c).to_csv('Files/testset_RMSE.csv')

predictedTraffic = np.load("Files/testset_predictions_all_samples.npy")
actualTraffic = np.load("Files/testset_predictions_gtruths_all_samples.npy")
errorPerEdge = np.loadtxt("Files/testset_RMSE.csv", delimiter=',')

airportCoordinateReader = pd.read_csv("Files/Airport_to_Coordinates.csv", delimiter=',', skiprows=0, low_memory=False)
airportConnectionReader = pd.read_csv("Files/Airport_Connections_coordinates.csv", delimiter=',', skiprows=0, low_memory=False)
airportNameReader = pd.read_csv("Files/Airport_to_Name.csv", delimiter=',', skiprows=0, low_memory=False)

airportConnectionNames = []
airportXYCoordinates = []
airportsToBePlotted = []

DECIMAL_TO_INT_FACTOR = 6

print("(Traffic Density Prediction = 0) (Traffic Density Actual = 1) (Error Per Edge = 2):", end=" ")
decision = int(input())

if decision == 0:
    arrayToBePlotted = predictedTraffic
elif decision == 1:
    arrayToBePlotted = actualTraffic
elif decision == 2:
    arrayToBePlotted = errorPerEdge

print("Input Prediction Steps (1 to 5):", end=" ")
predictionStep = int(input()) - 1

if decision == 0 or decision == 1:
    print("Input Time Steps (1 to MAX):", end=" ")
    timeStep = int(input()) - 1

print("Input Graph Density (Higher Values Are Less Dense):", end=" ")
graphDensity = int(input())

geometry = [Point(xy) for xy in zip(airportCoordinateReader['Longitude'], airportCoordinateReader['Latitude'])]
gdf = GeoDataFrame(airportCoordinateReader, geometry=geometry)

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world.plot(color='#0f4b7e')

for row in zip(airportConnectionReader['Airport 1'], airportConnectionReader['Airport 2']):
    airportConnectionNames.append((row[0].strip(), row[1].strip()))

for i in range(len(gdf)):
    airportXYCoordinates.append((gdf['geometry'][i].coords[0][0], gdf['geometry'][i].coords[0][1]))

for i in range(len(airportConnectionNames)):

    if i % graphDensity == 0:

        if decision == 0 or decision == 1:
            plotEdge(airportXYCoordinates[findAirportIndex(airportConnectionNames[i][0], airportNameReader)], airportXYCoordinates[findAirportIndex(airportConnectionNames[i][1], airportNameReader)], arrayToBePlotted[timeStep, predictionStep, i], np.nanmin(arrayToBePlotted[timeStep, predictionStep]), np.nanmax(arrayToBePlotted[timeStep, predictionStep]))
        elif decision == 2:
            arrayToBePlotted[predictionStep, i] = arrayToBePlotted[predictionStep, i] * (10 ** DECIMAL_TO_INT_FACTOR)
            plotEdge(airportXYCoordinates[findAirportIndex(airportConnectionNames[i][0], airportNameReader)], airportXYCoordinates[findAirportIndex(airportConnectionNames[i][1], airportNameReader)], int(arrayToBePlotted[predictionStep, i]), np.nanmin(arrayToBePlotted[predictionStep]), np.nanmax(arrayToBePlotted[predictionStep]))

        airportsToBePlotted.append(airportConnectionNames[i][0])
        airportsToBePlotted.append(airportConnectionNames[i][1])

for i in range(len(airportsToBePlotted)):

    plt.plot(airportXYCoordinates[findAirportIndex(airportsToBePlotted[i], airportNameReader)][0], airportXYCoordinates[findAirportIndex(airportsToBePlotted[i], airportNameReader)][1], marker="o", markersize=5, markeredgecolor="black", markerfacecolor="red")

plt.show()