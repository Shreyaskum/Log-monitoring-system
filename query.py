#!/usr/bin/env python3
import dns
import sys
import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure,OperationFailure

try:
    file = sys.argv[1]  #getting file from argument
    f = open(file,"r")  #reading contents from the file
    contents = f.readlines()  
    final = []
    for i in range(1,len(contents)):  #Storing the file contents in the desired format in final array using the for loop
        arr = contents[i].split(" ")
        b = []
        for x in arr:
            if len(x) != 0 and x!='\n':
                b.append(x)
        final.append(b)

    for j in range(len(final)):
        a = int(final[j][0])
        final[j][0] = a 
except:
    print("Plesae enter the proper file path")
    exit()


try:
    client = MongoClient('localhost',27017) #Connecting to MongoDB
    db = client.QUANTIL
    collection = db.data
    # for i in range(len(final)):   #Inserting values into MongoDB using for loop
    #     mydict = {"timestamp":final[i][0],"IP":final[i][1],"cpu_id":final[i][2],"usage":final[i][3]}
    #     x = collection.insert_one(mydict)     
    # print("Initialization complete")
except ConnectionFailure:
    print("MongoDB error occured")
    exit()
except OperationFailure:
    print("MongoDB operation error occured")
    exit()
except Exception as e:
    print("MongoDb error occured. The error is",e)
    exit()

while True:
    while True:
        # getting input from user 
        g = input("Please enter the query: The format is as follows: IP CPU_ID start_time(YYYY-MM-DD HH:MM) end_time(YYYY-MM-DD HH:MM) or type EXIT to terminate: ")
        if(g.strip() == "EXIT"):
            exit()
        user_data = g.split(" ")
        final_data = []
        for i in user_data: # passing data into final_data array in desired format
            if(len(i)>0):
                final_data.append(i)
        if(len(final_data) == 6 and (final_data[1] == "0" or final_data[1]== "1")):
            break   
        else:
            print("Input is incorrect")   

    try:
        print("CPU",final_data[1],"usage on",final_data[0],":")

        start = final_data[2]+" "+final_data[3]
        #converting user data into timestamp for comparison
        date_time_obj = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M') 
        start_timestamp = int(datetime.datetime.timestamp(date_time_obj))

        end = final_data[4]+" "+final_data[5]
        date_time_obj1 = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M')
        end_timestamp = int(datetime.datetime.timestamp(date_time_obj1))
        
    except:
        print("Start and end time are in incorrect format")
        exit()
        
    # Queruy for getting value MongoDB based on user input
    qu = collection.find({"$and":[{"timestamp":{"$gte" :start_timestamp,"$lte" :end_timestamp},"IP":final_data[0],"cpu_id":final_data[1]}]})
    c = 0
    for doc in qu:
        a = ((datetime.datetime.fromtimestamp(doc['timestamp'])))
        b = a.strftime('%Y-%m-%d %H:%M')
        print("("+b+","+(doc['usage'])+"%)")
        c+=1
    if(c==0):
        print("Sorry no match found for given input")
