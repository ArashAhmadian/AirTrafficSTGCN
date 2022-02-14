import csv
from random import random

# http://ww2.amstat.org/sections/graphics/datasets/DataExpo2009.zip
# https://www.transtats.bts.gov/DataIndex.asp

def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += (ele + ",")

    str1 = str1[:-1]
    # return string
    return str1


year = input("Write the year file to be sorted: ")
with open('sorted_' + str(year) + '.csv', 'w') as outfile:
    with open('short_' + str(year) + '.csv', mode='r') as infile:
        print("Reading " + str(year))
        reader = list(csv.reader(infile))  # load the whole file as a list
        length = len(reader)
        header = reader[0]  # the first line is your header
        outfile.write(listToString(header) + '\n')
        i = 0
        sorted2 = sorted(reader[1:], key=lambda row: (int(row[0]), int(row[1]), int(row[2])))
        for row in sorted2:
            outfile.write(listToString(row) + '\n')
    print(str(year) + " shortened")