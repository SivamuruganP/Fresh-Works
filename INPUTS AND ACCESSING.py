#Accessing and performing operations on MAINFILE by:

# Importing the MAIN_FILE as Library and runnning the MODULES of the MAIN_FILE

#SYNTAX: import FILE_NAME as Variable_name (any variable name)

import Freshworks as sp
#now the MAINFILE is imported as library

#FOR Creating a key without Time-To-Live Property
#SYNTAX sp.create(key,value)
sp.create("Freshworks",800)

#FOR Creating a key with Time-To-Live Property
#SYNTAX sp.create(key,value,time_out)

sp.create("Fresh",5300,40)  #time_out value in seconds

#For Read operation 
#SYNTAX sp.read(key)

sp.read("Freshworks")
#This returns the value of the given particular key in JSON object format 'key:value'

sp.read("Fresh")
#This returns the value of the given particular key in JSON object format 'key:value' if the TIME-TO-LIVE is NOT EXPIRED else ERROR message will be printed

#if you are creating a duplicate key 
sp.create("Freshworks",50)
#This returns an ERROR since the given key already exists in the database so another key must be given

#For Delete operation
#SYNTAX sp.delete(key)

sp.delete("Freshworks")
#This deletes the given particular key and its value from the database

#THREADS

# ACCESS using multiple threads :
#Thread 1
t1=threading.Thread(target=create,args=(key,value,timeout)) #for Create operation
t1.start()

#Thread 2
t2=threading.Thread(target=read,args=(key,)) #for Read operation
t2.start()

#Thread 3
t2=threading.Thread(target=delete,args=(key,)) #for Delete operation
t2.start()
# until  tn i.e Thread n and for given threads
