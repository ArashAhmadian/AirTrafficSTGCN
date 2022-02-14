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


year = input("Write the year file to be shortened: ")
percentage = float(input("Percentage of the original file to keep (random lines): "))
with open('short_' + str(year) + '.csv', 'w') as outfile:
    with open(str(year) + '.csv', mode='r') as infile:
        print("Reading " + str(year))
        reader = list(csv.reader(infile))  # load the whole file as a list
        length = len(reader)
        header = reader[0]  # the first line is your header
        outfile.write(listToString(header) + '\n')
        i = 0
        for row in reader[1:]:  # content is all the other lines
            i += 1
            if i % 10000 == 0:
                print("Line: " + str(i) + " / " + str(length))
            if random() < (percentage/100.0):
                outfile.write(listToString(row) + '\n')
    print(str(year) + " shortened")
