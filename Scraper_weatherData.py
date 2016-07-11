# Python 2.7
# Import the libraries

import csv
import urllib
from BeautifulSoup import *
import re

#Open a CSV File for write mode
f=open('Weather_Data3.csv','w')
##writer = csv.writer(f,lineterminator = '\n')

#Read the unique values of the City,state combination from the FILE StoreData.csv
with open('StoreData.csv', 'rb') as csvfile:
	next(csvfile)                           ## Ignore the header
	DataCaptured = csv.reader(csvfile, delimiter=',') ## Reading the file
	City, State = [],[]                     ##Initiallizing the variable for storing city and state
	for row in DataCaptured:				## Looping over all the rows of the data
	  if (row[2].title()) not in City:		## Checking for the unique values of City
		City.append(row[2].title())			##If the value doesn't exist in the list add the city
		State.append(row[3])				##Add the correspoding state 
	
## Extracting the daily weather information for each city with the specified year range

for i in range(1,len(City)):   ## to loop over all the city, state pair
	city=City[i]				
	state =State[i]
	f.write(city)
	f.write(state)
	urlbase="https://www.wunderground.com/cgi-bin/findweather/getForecast?query={0}%09{1}".format(city,state) ##Get the base url for particular city
	html = urllib.urlopen(urlbase).read() ##Open the url and read the page
	soup = BeautifulSoup(html)    
	tags = soup('a')		## Extract all anchor tags
	for tag in tags:         ## Loop over all the tags to get the url for the monthly calendar
		url= str(tag.get('href', None))
		if "MonthlyCalendar" in url:
			urlf=url
		
	#print urlf
## Using Regular Expression

	airport= re.findall('airport/(\S+)/2016',urlf)  ## Extract the airport name from the URL for the corresponding city, datatype is list
	Zipcode= re.findall('.zip=(\S+)&reqdb.m',urlf)	## Extract the zipcode for the corresponding city
	magic= re.findall('.magic=(\S+)&reqdb.wmo',urlf) ## Extract the unique magic value used by the url for the corresponding city

	#Looping over the year range
	for year in range(2010,2014):
		
		#Looping over the all the months
		for month in range(1,13):
		
			#Getting the URL by inserting the value of airport code, year, month, city, state, zipcode magic value
			url1="https://www.wunderground.com/history/airport/{0}/{1}/{2}/11/MonthlyHistory.html?req_city={3}&req_state={4}&reqdb.zip={5}&reqdb.magic={6}&reqdb.wmo=99999&format=1".format(airport[0],year,month,city,state,Zipcode[0],magic[0])
			#print url1
			html1 = urllib.urlopen(url1).read()  ##Read teh page with the monthly history data corresponding to the City 
			soup1 = BeautifulSoup(html1)  ## Converting the page using beautiful soup
			data1= soup1.prettify()
			for row in data1:
				f.write(row)  		## Write the data into the csv file
				