import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt, pylab
from collections import OrderedDict
import os.path
#import googlemaps
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
    global allDistricts, cnts, dist_cnts_sort, keys
    allDistricts, cnts = np.unique(npdata[DISTRICT], return_counts=True)
    district_cnts = dict(zip(allDistricts, cnts))
    
    #Since district 31 has only 2 offenses and no arrest I have eliminated 
    # to be able to make arrays of same length 
    allDistricts = allDistricts[:-1]
    cnts = cnts[:-1]
    
    #sort the dictionary by value and capture the top 3 districts 
    dist_cnts_sort = OrderedDict(sorted(district_cnts.items(), key=lambda x: x[1]))
    keys = np.fromiter(dist_cnts_sort.keys(), dtype=int)
    keys = keys[1:]
    d3, d2, d1 = keys[-3:]
    
    print("Offenses for the top 3 districts")
    
    #create a unique array of the offenses for the top 3+ districts
    #create bar graphs for each of the top 3 districts
    d1_off, cnt = np.unique(npdata[npdata[DISTRICT]==d1][[PRIMARYTYPE]], return_counts=True)
    plt.figure(figsize=(8,9))
    plt.title("1st Highest in Offenses: District " + str(d1))
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
    
def distBottom3(npdata):
    print("\nBottom 3 Districts with the Lowest Offenses")
    b1, b2, b3 = keys[0:3]
   
    b1_off, cnt = np.unique(npdata[npdata[DISTRICT]==b1][[PRIMARYTYPE]], return_counts=True)
    plt.figure(figsize=(8,9))
    plt.title("1st Lowest in Offenses: District " + str(b1))
    plt.ylabel("Offenses")
    plt.xlabel("Number of Offenses")
    plt.barh(b1_off, cnt)
    plt.show()
    
    b2Off, cnt = np.unique(npdata[npdata[DISTRICT]==b2][[PRIMARYTYPE]], return_counts=True)
    plt.figure(figsize=(8,9))
    plt.title("2nd Lowest in Offenses: District " + str(b2))
    plt.ylabel("Offenses")
    plt.xlabel("Number of Offenses")
    plt.barh(b2Off, cnt)
    plt.show()
    
    
    b3Off, cnt = np.unique(npdata[npdata[DISTRICT]==b3][[PRIMARYTYPE]], return_counts=True)
    plt.figure(figsize=(8,9))
    plt.title("3rd Lowest in Offenses: District " + str(b3))
    plt.ylabel("Offenses")
    plt.xlabel("Number of Offenses")
    plt.barh(b3Off, cnt)
    plt.show()
    
    

#show the number of arrest for each distric
def arrestByDist(npdata):
    #create an array of all arrest, and all districts, 
    #counts the districts and create a dictionary with the # of arrest
    #and the number of offenses
    global all_arrest, district, arrest
    
    all_arrest = npdata[npdata[ARREST] == True][[DISTRICT]]
    district, arrest = np.unique(all_arrest, return_counts=True)
    
    
  
    #create bar graph
    plt.figure(figsize = (10,8))
    plt.title("Number of Offenses and Arrest")
    plt.ylabel("District")
    plt.xlabel("Number of Arrest")
    plt.yticks((allDistricts))
    plt.barh(allDistricts, cnts, color = 'orange', label='All Offenses')
    plt.barh(district, arrest, color = 'blue', label='Arrest')
    plt.legend()
    plt.show()

#arrest percent for each district -- looking to find differences in arrest
#for each district
def arrest_percent(npdata):

    percent = cnts / arrest
    
    dist_arrest_percent = dict(zip(district, percent))
    dist_arrest = dict(zip(district, arrest))
    dist_offense = dict(zip(district, cnts))
    
    
    plt.figure(figsize = (8,9))
    plt.title("Perctage of arrest for each District")
    plt.ylabel('District')
    plt.xlabel('Arrest Percentage')
    plt.yticks((allDistricts))
    plt.barh(allDistricts, percent)
    plt.show()
    
  ##information for districcts w/ most / least arrest perccent
    maxp = max(dist_arrest_percent, key=lambda key: dist_arrest_percent[key])
    minp = min(dist_arrest_percent, key=lambda key: dist_arrest_percent[key])
    
    
    print("Highest Percentage district : ",  maxp,
          "\nPercent of Arrest to Offenses; ", '{:.2f}%'.format(dist_arrest_percent[maxp]),
          "\nNumber of Arrest: ", dist_arrest[maxp],
          "\nNumber of Offenses: " , dist_offense[maxp])
    
    print("\nLowest Percitage district : ", minp,
          "\nPercent of Arrest to Offenses: ", '{:.2f}%'.format(dist_arrest_percent[minp]),
          "\nNumer of Arrest: ", dist_arrest[minp],
          "\nNumber of Offenses: ", dist_offense[minp], "\n")
   
    
#will compare the amount of arrest to offenses for all crimes in district 11
#district 11 has the lowest arrest but the highest offenses    
def low_perc_dist(npdata):

    d11 = npdata[npdata[DISTRICT]==11]
    d11_df = pd.DataFrame(d11, columns = [PRIMARYTYPE,ARREST])
    
    d11_off_uniq = pd.value_counts(pd.Series(d11_df[PRIMARYTYPE]))
    
    d11_arrest = d11_df.loc[lambda d11_df: d11_df[ARREST]==True]
    d11_arrest_uniq = pd.value_counts(pd.Series(d11_arrest[PRIMARYTYPE]))
    
    df = pd.concat([d11_off_uniq, d11_arrest_uniq], sort=False,axis = 1,
                   keys=['offenses','arrest'], names=['District 11'])
    df = df.fillna(0)
 
    print(df,"\n")
    df.plot(kind='barh',figsize=(8,9), legend=True)
    plt.title("District 11 Offenses and Arrest")
    plt.xlabel("Number of Offenses")
    plt.ylabel("Offenses")
    
def high_perc_dist(npdata):
    
    df17 = pd.DataFrame(npdata[npdata[DISTRICT]==17], columns =[PRIMARYTYPE, ARREST])
    df17_off_uniq = pd.value_counts(pd.Series(df17[PRIMARYTYPE]))
    
    df17_arr = df17.loc[lambda df17: df17[ARREST]==True]
    df17_arr_uniq = pd.value_counts(pd.Series(df17_arr[PRIMARYTYPE]))
    
    df = pd.concat([df17_off_uniq, df17_arr_uniq], sort=False, axis=1,
                    keys=['offenses','arrest'], names=['District 17'])
    df = df.fillna(0)
    
   
    
    df.plot(kind='barh', figsize=(8,9), legend=True)
    plt.title("District 17 Offenses and Arrest")
    plt.xlabel("Number of Offenses")
    plt.ylabel("Offenses")
    
    print(df,"\n")
    
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

    
def violentVsNonviolentCrimesForChicago(npdata):
    vCrimes = []
    nvCrimes = []
    #print(npdata[PRIMARYTYPE])
    for i in npdata[PRIMARYTYPE]:
        #print(i)
        if(i == 'ARSON' or
            i == 'ASSAULT' or
            i == 'BATTERY' or
            i == 'BURGLARY' or
            i == 'CRIMINAL DAMAGE' or
            i == 'HOMICIDE' or
            i == 'HUMAN TRAFFICKING' or
            i == 'INTIMIDATION' or
            i == 'KIDNAPPING' or
            i == 'OFFENSE INVOLVING CHILDREN' or
            i == 'ROBBERY' or
            i == 'WEAPONS VIOLATION'):
                vCrimes.append(i)
        elif(i == 'NON-CRIMINAL' or
            i == 'NON-CRIMINAL (SUBJECT SPECIFIED)' or
            i == 'OTHER OFFENSE'):
            continue;
        else:
            nvCrimes.append(i)
            
    numv = len(vCrimes)
    numnv = len(nvCrimes)
    
    labels = ['Non-violent', 'Violent']
    slices = [numnv, numv]
    colors = ['royalblue', 'firebrick']
    
    plt.pie(slices, labels=labels, colors=colors, explode=[0, .1], autopct='%1.1f%%', shadow=True, radius=2)
    plt.title('Violent vs. Non-violent Crimes in Chicago', pad=150)
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
    distBottom3(data)
    arrestByDist(data)
    arrest_percent(data)
    low_perc_dist(data)
    high_perc_dist(data)
    timeOfCrime(data)
    topCrimeTimes(data)
    showCrimeByZipcode2018(data)
    showCrimeByMonth2018(data)
    violentVsNonviolentCrimesForChicago(data)
    

if __name__ == "__main__":
    main()
