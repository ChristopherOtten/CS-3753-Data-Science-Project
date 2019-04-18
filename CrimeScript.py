import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt, pylab

#constants to quickly references the columns
BLOCK = 'Block'
PRIMARYTYPE = 'Primary Type'
LOCATIONDESCRIPTION = 'Location Description'

#function to read the crime statistics file and return
#a clean dataframe
def getCleanCrimeData():
    data = pd.read_csv('Crimes_-_2017_to_present.csv')
    data = data.dropna()
    return data

#Each problem should be kept in a function, Example
#function below in which takes in a dataframe and prints
#the data types
def funcExample(data):
    print(data.dtypes)

#Gather 10 most dangerous areas, display occurences, and top crimes committed
def topCrimeBlocks(npdata):
    
    #returns 2 arrays, one for all blocks, another for number of times
    #blocks appear
    allBlocks, counts = np.unique(npdata[BLOCK], return_counts=True)
    print("\nTen Chicago Blocks With Highest Crimes Reported:\n")
    
    #finds and prints 10 most crime ridden blocks and 2 most common offenses
    for i in range(0,10):
        
        #gets most common crime and location
        blockIndex = counts.argmax()
        total = counts[blockIndex]
        block = allBlocks[blockIndex]
        
        #delete crime/location to not allow duplicates
        counts = np.delete(counts,blockIndex)
        allBlocks = np.delete(allBlocks,blockIndex)
        
        #get most common crime in specific location
        crimes = npdata[npdata[BLOCK]==block]
        allCrimes, c = np.unique(crimes[PRIMARYTYPE], return_counts=True)
        
        #find 2 most common crimes, delete entries to not allow duplicates
        crimeIndex = c.argmax()
        offense1 = allCrimes[crimeIndex]
        c = np.delete(c,crimeIndex)
        allCrimes = np.delete(allCrimes,crimeIndex)
        crimeIndex = c.argmax()
        offense2 = allCrimes[crimeIndex]
        
        #get most common location of crimes
        location = npdata[npdata[BLOCK]==block]
        allLocations, co = np.unique(crimes[LOCATIONDESCRIPTION], return_counts=True)
        
        #find 2 most location of crimes, delete entries to not allow duplicates
        localIndex = co.argmax()
        location1 = allLocations[localIndex]
        co = np.delete(co,localIndex)
        allLocations = np.delete(allLocations,localIndex)
        localIndex = co.argmax()
        location2 = allLocations[localIndex]
        
        #print results
        print("Block: ",block,"\nOccurences:",total," \nMost Common Offenses:",offense1,",",offense2,"\nMost Common Locations:",location1,",",location2,"\n")
        
def leastCrimeBlocks(npdata):
    
    #returns 2 arrays, one for all blocks, another for number of times
    #blocks appear
    allBlocks, counts = np.unique(npdata[BLOCK], return_counts=True)
    
    al = np.array(['0'])
    
    #finds and prints 10 most crime ridden blocks
    for i in range(0,100):
        blockIndex = counts.argmin()
        total = counts[blockIndex]
        block = allBlocks[blockIndex]
        
        crimes = npdata[npdata[BLOCK]==block]
        al = np.append(al,crimes[PRIMARYTYPE])
        allC = np.unique(al)
    
    allC = ' '.join(allC[1:])
    print("Most Common Crime Among 100 Least Dangerous Areas:",allC)

#create bar chart of total offenses
def barOffenses(npdata):
    
    allCrimes, c = np.unique(npdata[PRIMARYTYPE], return_counts=True)
    
    plt.figure(figsize=(8,9))
    plt.barh(allCrimes,c)
    plt.show()
    print("Total Amount of Crimes Committed:",c.sum())
    
#sort the crimes and counts tuple of arrays and then "folds" them so that small and large entries are 
#altenrating in order to keep labels from overlapping. 
#returns the two arrays, sorted and folded
def sortAndFoldCrimes(data):
    data1, data2 = data
    #sort highest to lowest
    for i in range(0, len(data2)):
        for j in range(i, len(data2)):
            if(data2[j] > data2[i]):
                temp2 = data2[i]
                data2[i] = data2[j]
                data2[j] = temp2
                
                temp1 = data1[i]
                data1[i] = data1[j]
                data1[j] = temp1
    
    #fold the data
    fdata1 = []
    fdata2 = []
    
    i = 0
    j = len(data1) - 1
    while(j >= i):
        fdata1.append(data1[i])
        if j != i:
            fdata1.append(data1[j])
        
        fdata2.append(data2[i])
        if j != i:
            fdata2.append(data2[j])
        
        i += 1
        j -= 1
        
    #print (fdata2)
    #print(fdata1)
    return (fdata1, fdata2)

#create pie chart of count of each offense
def pieOffenses(npdata):
    
    #make two arrays, one of the crimes and the other of the counts for each crime, send them to be sorted
    #and "folded" so that small and large entries are altenrating in order to keep labels from overlapping
    crimes, counts = sortAndFoldCrimes(np.unique(npdata[PRIMARYTYPE], return_counts=True))
    
    #set the explode values so that the smaller ones are exploded more than the large
    explode = []
    for i in range(0, len(counts)):
        exVal = 0.125 - ( ( ( counts[i]/sum(counts) ) * 0.125) / 2)
       # exVal = 0.13
       # if(counts[i] < (sum(counts) * 0.01)):
        if(i % 2 == 1):
            exVal = exVal * 2.5
        explode.append(exVal)
    
    # Plot
    plt.pie(counts, explode=explode, labels=crimes, labeldistance=1.05, pctdistance=0.9, autopct='%1.1f%%', radius=3.8 )
    plt.title('Percentage of Crimes by Offense', pad=280)
    plt.show()
    
def districtTop3(npdata):
    #create a unique array of the districts and create a dict
    allDistricts, cnts = np.unique(npdata[DISTRICT], return_counts=True)
    district_cnts = dict(zip(allDistricts, cnts))
    
    #sort the dictionary by value and capture the top 3 districts 
    dist_cnts_sort = OrderedDict(sorted(district_cnts.items(), key=lambda x: x[1]))
    keys = np.fromiter(dist_cnts_sort.keys(), dtype=int)
    d3, d2, d1 = keys[-3:]
    
    print("Offenses for the top 3 districts")
    
    #create a unique array of the offenses for the top 3+ districts
    #create bar graphs for each of the top 3 districts
    d1_off, cnt = np.unique(npdata[npdata[DISTRICT]==d1][[PRIMARYTYPE]], return_counts=True)
    plt.figure(figsize=(8,9))
    plt.title("District " + str(d1) + "\n#1 in Offenses")
    plt.ylabel("Offenses")
    plt.xlabel("Number of Offenses") 
    plt.barh(d1_off, cnt)
    plt.show()
    
    d2_off, cnt = np.unique(npdata[npdata[DISTRICT]==d2][[PRIMARYTYPE]], return_counts=True)
    plt.figure(figsize=(8,9))
    plt.title("District " + str(d2) + "\n#2 in Offenses")
    plt.ylabel("Offenses")
    plt.xlabel("Number of Offenses") 
    plt.barh(d2_off, cnt)
    plt.show()
    
    d3_off, cnt = np.unique(npdata[npdata[DISTRICT]==d2][[PRIMARYTYPE]], return_counts=True)
    plt.figure(figsize=(8,9))
    plt.title("District " + str(d3) + "\n#1 in Offenses")
    plt.ylabel("Offenses")
    plt.xlabel("Number of Offenses") 
    plt.barh(d3_off, cnt)
    plt.show()

    
#main function in which runs all functions, no logic in main only reference
#to another function

#when pushing to the repo make sure to comment our your function
#at the end we can uncomment and run. 
def main():
    # only read from file once, use data in other functions
    data = getCleanCrimeData()
    
    #example function for each problem
    #funcExample(data)
    
    topCrimeBlocks(data)
    leastCrimeBlocks(data)
    barOffenses(data)
    pieOffenses(data)
    districtTop3(data)

if __name__ == "__main__":
    main()
