#!/bin/python

import urllib.request
import http.client
import os

# Set the HTTP version to 1.0 (this avoids incomplete read errors)
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

# Command to extract titles from Pornhub's top rated page as of 5/4/2017
# Firstly this isolates the titles themselves, then after some necessary
# transformations, I run sort and uniq to get a count of each word, I then
# eliminate meaningless terms such as and and for, lastly all the data is
# put into csv format
bashExtract = '''cat stats.txt | grep -e '<a href.*title=\".*</a>' | sed 's/.*"//g' | 
                 tr -d '<>' | sed 's/\/a$//g' | sed '/\/a/d' | sed "s/&#039;/\'/g" | 
                 tr ' ' '\n' | tr A-Z a-z | sort | uniq -c | tr -s ' ' | sort -nr | 
                 sed '/[12] /d' | sed '/-$/d' | sed '/ to$/d' | sed '/ of$/d' | 
                 sed '/ it$/d' | sed '/ me$/d' | sed '/ my$/d' | sed '/ in$/d' | 
                 sed '/ with$/d' | sed '/ at$/d' | sed '/ and$/d' | 
                 sed '/ the$/d' | sed '/ a$/d' | sed '/ for$/d' | sed 's/^ //g' | 
                 tr ' ' ',' >> results.csv'''

# stats.txt is an intermediate file used to hold GET data
dataFile = open('stats.txt', 'wb+')

# Get data from the first n pages where n is the range
for i in range(1,10):
    # As of 5/4/2017 Pornhub's top rated pages use this url format
    url = "https://www.pornhub.com/video?o=tr&page=%d"%(i)
    # Send an HTTP GET request and read the data
    request = urllib.request.urlopen(url)
    try:
        data = request.read()
    except http.client.IncompleteRead as  e:
        data = e.partial
    # Write the data into a file that will be parsed for titles later
    dataFile.write(data)
    request.close()

# Extract the titles from the raw data and write them to results.txt
os.system('echo value,id > results.csv')
os.system('echo 0,empty >> results.csv')
os.system(bashExtract)
# Clean up the intermediate file
os.system('rm stats.txt')
dataFile.close()
