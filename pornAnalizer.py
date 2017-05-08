#!/bin/python

import urllib.request
import http.client
import os
import threading
from queue import Queue

q = Queue()
file_lock = threading.Lock()

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
                 sed '/ with$/d' | sed '/ at$/d' | sed '/ and$/d' | sed '/ &amp;$/d' | 
                 sed '/ the$/d' | sed '/ a$/d' | sed '/ for$/d' | sed 's/^ //g' | 
                 tr ' ' ',' >> results.csv'''

# stats.txt is an intermediate file used to hold GET data
dataFile = open('stats.txt', 'wb+')

def getPage(n):
    # As of 5/4/2017 Pornhub's top rated pages use this url format
    url = "https://www.pornhub.com/video?o=tr&page=%d"%(n)
    # Send an HTTP GET request and read the data
    request = urllib.request.urlopen(url)
    try:
        data = request.read()
    except http.client.IncompleteRead as  e:
        data = e.partial
    # Write the data into a file that will be parsed for titles later
    with file_lock:
        dataFile.write(data)
    request.close()

# handles multithreading capabilities, pulls a worker from the queue of tasks
# and pscans the port number specified by that worker
def threader():
    while True:
        worker = q.get()
        getPage(worker)
        q.task_done()

for x in range(30):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

for worker in range(1,30):
    q.put(worker)

q.join()

# Extract the titles from the raw data and write them to results.txt
os.system('echo value,id > results.csv')
# Adding this empty line ensures that the d3 visualization will not discard the
# real first value
os.system('echo 0,empty >> results.csv')
os.system(bashExtract)
dataFile.close()
# Clean up the intermediate file
os.system('rm stats.txt')
