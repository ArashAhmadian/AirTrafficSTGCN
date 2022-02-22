import csv
import os
import numpy as np 
import pandas as pd

from numpy import NaN, short 
from random import random

# http://ww2.amstat.org/sections/graphics/datasets/DataExpo2009.zip
# https://www.transtats.bts.gov/DataIndex.asp


#convert list to string 
def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += (ele + ",")

    str1 = str1[:-1]
    # return string
    return str1

file_path=os.path.abspath('.')

#year: year of file to shortened
#percentage: percentage of original file to keep
#shorten the given data. 
def shortener(year,percentage):
    try:
        short_path= os.path.abspath('./short_data/short_' + str(year) +'_'+str(percentage)+'%.csv')
        with open(short_path, 'w') as outfile:
            try:
                raw_path=os.path.abspath('./raw_data/DataExpo2009/'+str(year) + '.csv')
                with open(raw_path, mode='r') as infile:
                    reader = list(csv.reader(infile))  # load the whole file as a list
                    length = len(reader)
                    header = reader[0]  # the first line is your header
                    outfile.write(listToString(header) + '\n')
                    for row in reader[1:]:  # content is all the other lines
                        if random() < (percentage/100.0):
                            outfile.write(listToString(row) + '\n')

            except IOError: 
                print (raw_path)
    except IOError: 
        print (short_path)
    
    print(str(year) +'_'+str(percentage)+ "%"+'shortened')

#year: year of file to shortened
#percentage: percentage of original file to keep
#sort the data based on date.       
def sorter(year,percentage): 
    file_path=os.path.abspath('.')
    try:
        sort_path=os.path.abspath('./sorted_data/sort_'+str(year) +'_'+str(percentage)+'%.csv')
        with open(sort_path, 'w') as outfile:
            try:
                short_path= os.path.abspath('./short_data/short_' + str(year) +'_'+str(percentage)+'%.csv')
                with open(short_path, mode='r') as infile:
                    reader = list(csv.reader(infile))  # load the whole file as a list
                    length = len(reader)
                    header = reader[0]  # the first line is your header
                    outfile.write(listToString(header) + '\n')
                    sorted2 = sorted(reader[1:], key=lambda row: (int(row[0]), int(row[1]), int(row[2])))
                    for row in sorted2:
                        outfile.write(listToString(row) + '\n')

            except IOError: 
                print (short_path)
    except IOError: 
        print (sort_path)
    
    print(str(year) +'_'+str(percentage)+ "%"+'sorted')
        
#year: year of file to shortened
#percentage: percentage of original file to keep
#get rid of excess columns in the data. 
def cleaner(year,percentage): 
    clean_path= file_path+'\\cleaned_data\\'+'clean_' + str(year) +'_'+str(percentage)+'%'+ '.csv'
    sort_path= file_path+'\\sorted_data\\sort_' + str(year) +'_'+str(percentage)+'%.csv'
    header_list = ['Year','Month','DayofMonth','DayOfWeek','ActualElapsedTime','Origin','Dest']
    reader =  pd.read_csv(sort_path,usecols=header_list)
    nan_value = float("NaN")
    reader.replace("", nan_value, inplace=True)
    reader.dropna(inplace=True)
    #reader = reader.replace(r'^\s*$', np.NaN, regex=True)
    reader.to_csv(clean_path)
    print(str(year) +'_'+str(percentage)+ "%"+'cleaned')


if __name__=="__main__":
    for year in [2003,2004,2005,2006,2007,2008]: 
        print("===================================\n")
        shortener(year=year,percentage=56)
        sorter(year=year,percentage=56)
        cleaner(year=year,percentage=56)
        print("===================================\n")

    