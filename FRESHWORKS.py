import threading
import time
import json
from time import sleep
import os
dictionary = {}  # dictionary in which we store data

# for create operation syntax is "create(key_name,value,timeout_value)" timeout is optional you can continue by
# passing two arguments without timeout
lock = threading.Lock()

log_file = 'JSON_SRC_FILE.json'
if not os.path.exists(log_file):
    with open(log_file, 'w') as Json_FILE:
        json.dump([], Json_FILE)

def create(key, value, timeout=0):
    lock.acquire()
    with open(log_file) as json_file:
        data = json.load(json_file)
    if key in data:
        print("error: this key already exists")  
    else:
        if key.isalpha():
            json_obj = json.dumps(data)
            json_size = len(json_obj)
            if len(key) <= 32 and len(str(value)) <= (16*1000) and json_size <=134217728 :  # constraints for file size less than 1GB and Jsonobject value less than 16KB
                if timeout == 0:
                    list_val=[value,timeout]
                else:
                    list_val = [value, time.time() + timeout]
                
                dictionary[key] = list_val
                with open(log_file, 'w') as outfile:
                    json.dump(dictionary, outfile)
            else:
                print("ERROR: Memory limit exceeded!! ")  
        else:
            print("ERROR: Invalid key_name!! key must contain only alphabets and no special characters or numbers")  
    lock.release()

# for read operation
# syntax is "read(key)"

def read(key):
    lock.acquire()
    with open(log_file) as json_file:
        data = json.load(json_file)
    if key not in data:
        print("error: given key does not exist in database. Please enter a valid key")  
    else:
        b = data[key]
        if b[1] != 0:
            if time.time() < b[1]:  #comparing the present time with expiry time
                print('{' + str(key) + ':' + str(data[key][0]) +'}',end='')
                
            else:
                print(f"ERROR: TIME-TO-LIVE Of {key} has expired")  
        else:
            print('{' + str(key) + ':' + str(data[key][0]) +'}',end='')

    lock.release()
# for delete operation
# syntax is "delete(key_name)"

def delete(key):
    lock.acquire()
    with open(log_file) as outfile:
        data=json.load(outfile)
    
    if key not in data:
        print("ERROR: Given key does not exist in database. Please enter a valid key")  
    else:
        d={}
        b = data[key]
        if b[1] != 0:
            if time.time() < b[1]:  # comparing the current time with expiry time
                with open(log_file) as outfile:
                    data=json.load(outfile)
                for element in data:
                    if element!=key:
                        d[element]=data[element]
                        with open(log_file,'w') as data_file:        
                            json.dump(d, data_file)
                    
                print("key is successfully deleted")

            else:
                print("ERROR: TIME-TO-LIVE of", key, "has expired")  # error message5
        else:
            with open(log_file) as outfile:
                data=json.load(outfile)
            for element in data:
                if element!=key:
                    d[element]=data[element]
                    with open(log_file,'w') as data_file:        
                        json.dump(d, data_file)
            print("key is successfully deleted")
    lock.release()
