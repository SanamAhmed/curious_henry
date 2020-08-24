#!/usr/bin/python3

import _thread
import time
import json
import traceback
# Define a function for the thread
from DBHandler import DBHandler
from FileProcessor import FileProcessor
def process( threadName ):
   while True:
       with open('configurations.json') as f:
           data = json.load(f)

       DATABASEIP = data["DATABASEIP"]
       DB_USER = data["DB_USER"]
       DB_PASSWORD = data["DB_PASSWORD"]
       DATABASE = data["DATABASE"]
       THREAD_SLEEP_TIME = data["THREAD_SLEEP_TIME"]
       DBHandler_ = DBHandler(DATABASEIP,DB_USER,DB_PASSWORD,DATABASE)
       fileList =[]
       try:
           fileList = DBHandler_.getFilesToProcess()
           print("Going to process"+str(len(fileList))+"files")
           try:
               for file_ in fileList:
                   FileProcessor_  = FileProcessor()
                   FileProcessor_.process(file_)
           except Exception as e:
               print("Error in File Processing Thread" + str(e))
               print(traceback.format_exc())
               DBHandler_.updateFileStatus(file_.FileName, "F")


       except Exception as e:
           print("Error in File Processing Thread"+str(e))
           print(traceback.format_exc())


       print (threadName +"going to sleep for "+ str(THREAD_SLEEP_TIME))
       time.sleep(THREAD_SLEEP_TIME)




# Create two threads as follows
try:
   _thread.start_new_thread( process, ("FileProcessingThread", ) )

except:
   print ("Error: unable to start thread")

while 1:
   pass
