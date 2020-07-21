#!/usr/bin/env python3
import datetime
import random
tvalue = datetime.datetime(2014,10,31,0,0).timestamp()  # Getting the timestamp for 10/31/2014
startval = ((00)*3600 + (00)*60) #start time of the day
endval = ((23)*3600 + (60)*60) #end time of the day
count = 0
timeStampArr = []
IPSet = set()
IPArr = []
while (endval > startval):
    #Inserting values into timeStamp array
    timeStampArr.append(int(tvalue+startval))
    startval+=60
    count+=1

while(len(IPSet)<1000):
    #generating random IP's in IPv4 range
    a = str(random.randint(0,255))
    b = str(random.randint(0,255))
    randomIp = "192.169."+a+"."+b
    IPSet.add(randomIp)
for x in IPSet:
    IPArr.append(x)
       
f = open("data_log.txt","w+") # creating data_log file for writing data
# inserting title for each column
f.write("{: <15} {: <9} {: <8} {: <6}".format("timestamp","IP","cpu_id","Usage"))
f.write("\n")

#inserting data into the file aligned
for i in range(24*60):
        for j in range(1000):
            for k in range(2):
                f.write("{: <11} {: <16} {: <5} {: <3}".format(str(timeStampArr[i]),str(IPArr[j]),str(k),str(random.randint(0,100))))
                f.write("\n")

f.close()