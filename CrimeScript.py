import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt, pylab
from collections import OrderedDict
import os.path
import googlemaps
import math
import threading

#constants to quickly references the columns
BLOCK = 'Block'
PRIMARYTYPE = 'Primary Type'
LOCATIONDESCRIPTION = 'Location Description'
DISTRICT = 'District'
ARREST  = 'Arrest'
DATE = 'Date'
LATITUDE = 'Latitude'
LONGITUDE = 'Longitude'
YEAR = 'Year'
ZIPCODE = 'Zip'

# function to read the crime statistics file and return
# a clean dataframe
def getCleanCrimeData():
    filename = 'Crimes_-_2017_to_present.csv'
    # Return if filename exist, if not get data from github
    if os.path.isfile(filename):
        data = pd.read_csv(filename)
        data = data.dropna()
        return data
    else:
        getCleanCrimeDataFromWeb()

# function to read the crime statistics file and return
# a clean dataframe
def getCleanCrimeDataFromWeb():
    url = 'https://github.com/ChristopherOtten/CS-3753-Data-Science-Project/blob/master/Crimes_-_2017_to_present.csv'
    data = pd.read_csv(url)
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
    
#show the offenses for the top 3 districts
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

#show the number of arrest for each distric
def arrestByDist(npdata):
    #create an array of all arrest, counts the districts and create a dictionary with the # of arrest
    all_arrest = npdata[npdata[ARREST] == True][[DISTRICT]]
    district, arrest = np.unique(all_arrest, return_counts=True)
    dist_arrest_cnt = dict(zip(district, arrest))
  
    #create bar graph
    plt.figure(figsize = (8,9))
    plt.title("Number of arrest made in each district")
    plt.ylabel("District")
    plt.xlabel("Number of Arrest")
    plt.yticks(np.arange(1, 26, 1))
    plt.barh(district, arrest)
    plt.show()
    
def timeOfCrime(npdata):
    
    #get array of all times
    allTimes, counts = np.unique(npdata[DATE], return_counts=True)
    dayHours = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    #for each hour of day shown in dates, increment that index of dayHours
    for i in range(0,len(allTimes)):
        hour = allTimes[i][-5:-3]
        #print(hour)
        dayHours[int(hour)]+=1
    dayHours = np.asarray(dayHours)
    
    #plot results
    h = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
    plt.figure(figsize=(9,5))
    plt.plot(h,dayHours)
    plt.title("Time of Day for Crimes")
    plt.xlabel("Time of Day")
    plt.ylabel("Number of Crimes")
    plt.show()
    
    
def topCrimeTimes(npdata):
    
    top5 = ['THEFT', 'BATTERY', 'CRIMINAL DAMAGE', 'ASSAULT', 'OTHER OFFENSE']
    h = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
    for crime in top5:
        lines = npdata[npdata[PRIMARYTYPE]==crime]
        allTimes, counts = np.unique(lines[DATE], return_counts=True)
        dayHours = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
        for i in range(0,len(allTimes)):
            hour = allTimes[i][-5:-3]
            #print(hour)
            dayHours[int(hour)]+=1
        dayHours = np.asarray(dayHours)
        
        plt.figure(figsize=(9,5))
        plt.plot(h,dayHours)
        plt.title("Time of Day for %s" %crime)
        plt.xlabel("Time of Day")
        plt.ylabel("Number of %s Reported" %crime)
        plt.show()
        
#function to get data set from year 2018
def getDatafor2018(data):
    data = data[data[YEAR]==2018]
    return data

#Get zip code based on geographic coordinates using google's reverse geocoding api.
#Return 0 for a specific coordinate if not found or when an exception is thrown
#Note you will need to get a free trial in order to use thie api
#Insert api key below
def findZipcodeWithGoogle(data, zipCode, worker):
    gmaps = googlemaps.Client(key='insert key here')
    found = False
    for index, row in data.iterrows():
    # Look up an address with reverse geocoding
        try:
            reverse_geocode_result = gmaps.reverse_geocode((row[LATITUDE], row[LONGITUDE]))
            data = reverse_geocode_result[0]
            data = data['address_components']
            for key in data:
                if 'types' in key and 'postal_code' in key['types']:
                    zipCode.append(key['long_name'])
                    found = True
        except:
            print('error')
            zipCode.append(0)
            found = True
        if not found:
            zipCode.append(0)
        found = False

#Get the zip codes for year 2018 in dataset
#Partitions the dataset into 20 threads for faster retrieval of zip code
#Takes approx an hour to process
def getZipcodeData(data):
    zipcode_filename = 'zipcodes2018.csv'
    #Return if filename exist, if not get zip code data using threads
    if os.path.isfile(zipcode_filename):
        return pd.read_csv(zipcode_filename)
    else:
        data = getDatafor2018(data)
        num_of_threads = 20
        coordinates = data[[LATITUDE, LONGITUDE]]
        num_of_rows = len(coordinates.index)
        step = math.floor(num_of_rows / num_of_threads)
        start = 0
        threads = []
        zips = []
        for i in range(num_of_threads):
            arg = []
            res = []
            zips.append(res)
            if i == num_of_threads - 1:
                arg = coordinates[start:]
            else:
                arg = coordinates[start:start+step]
            t = threading.Thread(
                target=findZipcodeWithGoogle, args=(arg, res, i))
            t.start()
            threads.append(t)
            start += step
        for t in threads:
            t.join()

        zipConcat = []
        for zip in zips:
            zipConcat += zip
        data[ZIPCODE] = zipConcat
        data.to_csv(zipcode_filename)
        return data

#Displays the top 10 and least crimes by zip codes in 2018
def showCrimeByZipcode2018(data):

    data = getZipcodeData(data)
    data = data.reset_index(drop=True)
    data = data.drop('Unnamed: 0', axis=1)
    data = data[data[ZIPCODE] != 0]
    data = data.groupby([ZIPCODE]).size().sort_values(ascending=False)
    top10Worst = pd.DataFrame(data[:10])
    top10Best = pd.DataFrame(data[-10:])
    ax1 = top10Worst.plot(kind='bar', figsize=(10, 4), rot=0, legend=None, title='Top 10 Crimes Reported in Chicago in 2018')
    ax1.set_ylabel('Total Crimes Reported')
    ax1.set_xlabel('Zip Codes')

    ax2 = top10Best.plot(kind='bar', figsize=(10, 4), rot=0, legend=None, title='Top 10 Least Crimes Reported in Chicago in 2018')
    ax2.set_ylabel('Total Crimes Reported')
    ax2.set_xlabel('Zip Codes')

#Displays crimes by each month for 2018
def showCrimeByMonth2018(data):
    data = getDatafor2018(data)
    year = pd.DataFrame(data[DATE]).astype('str')
    year = year.applymap(lambda x: x.split('/')[0])
    year = year.groupby([DATE]).size().reset_index()

    year = year.astype(int)
    year = year.rename(columns={0: 'count'})
    year = year.sort_values([DATE])
    year.set_index(year[DATE], drop=True, append=False, inplace=True)
    year = year.drop(DATE, axis=1)
    ax1 = year.plot(kind='bar', figsize=(10, 4), rot=0, legend=None,
                          title='Monthly Crimes Committed in Chicago for 2018')
    ax1.set_ylabel('Total Crimes')
    ax1.set_xlabel('Month')
    ax1.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'])    
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
    arrestByDist(data)
    timeOfCrime(data)
    topCrimeTimes(data)
    showCrimeByZipcode2018(data)
    showCrimeByMonth2018(data)

if __name__ == "__main__":
    main()
