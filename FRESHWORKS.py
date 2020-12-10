import threading
import time
import json
from time import sleep
import os

dictionary = {}  

# program can also be run by passing two arguments without timeout
lock = threading.Lock()

log_file = 'SRC_FILE.json'
with open(log_file, 'w') as Json_FILE:
    json.dump([], Json_FILE)
        
def create(key, value, timeout=0):
    lock.acquire()
    with open(log_file) as json_file:
        data = json.load(json_file)

    if key in data:
        print("ERROR: This KEY already exists")

    else:
        if key.isalpha():
            json_obj = json.dumps(data)
            json_size = len(json_obj)
            if len(key) <= 32 and len(str(value)) <= (16 * 1000) and json_size <= 134217728:
                # constraints for file size less than 1GB and JSONObject value less than 16KB
                if timeout == 0:
                    list_val = [value, timeout]
                else:
                    list_val = [value, time.time() + timeout]

                dictionary[key] = list_val

                with open(log_file, 'w') as outfile:
                    json.dump(dictionary, outfile)
            else:
                print("ERROR : Memory limit exceeded!!... ")
        else:
            print("ERROR : INVALID KEY ! key name must contain only alphabets and no special characters or numbers")
    lock.release()


# Read operation syntax is "read(key)"

def read(key):
    lock.acquire()
    with open(log_file) as json_file:
        data = json.load(json_file)

    if key not in data:
        print("ERROR : given key does not exist in database. Please enter a valid key")

    else:
        val_dict_timeout = data[key]
        if val_dict_timeout[1] != 0:
            if time.time() < val_dict_timeout[1]:  # comparing the present time with expiry time
                print('{ ' + str(key) + ':' + str(data[key][0]) + ' }', end='')

            else:
                print(f"ERROR : TIME-TO-LIVE Of {key} has expired")
        else:
            print('{ ' + str(key) + ':' + str(data[key][0]) + ' }', end='')

    lock.release()


# Delete operation syntax is "delete(key)"

def delete(key):
    lock.acquire()
    with open(log_file) as outfile:
        data = json.load(outfile)
    count=0
    for key_count in data:
        count+=1
        if(count>1):
            break
    if key not in data:
        print("ERROR: Given key does not exist in database. Please enter a valid key")
    else:
        dict_data = {}
        val_in_dict_timeout = data[key]
        if val_in_dict_timeout[1] != 0:
            if time.time() < val_in_dict_timeout[1]:  # comparing the current time with expiry time
                if count>1:
                    with open(log_file) as outfile:
                        data = json.load(outfile)
                    for element in data:
                        if element!= key:
                            dict_data[element] = data[element]
                            with open(log_file, 'w') as data_file:
                                json.dump(dict_data, data_file)       
                else:
                    with open(log_file, 'w') as data_file:
                        json.dump([], data_file)
                del dictionary[key]
                print("KEY is deleted Successfully")
            else:
                print("ERROR: TIME-TO-LIVE of", key, "has expired")
        else:
            if count>1:
                with open(log_file) as outfile:
                    data = json.load(outfile)
                for element in data:
                    if element != key:
                        dict_data[element] = data[element]
                        with open(log_file, 'w') as data_file:
                            json.dump(dict_data, data_file)
            else:
                with open(log_file, 'w') as data_file:
                    json.dump([], data_file)
            del dictionary[key]
            print("KEY is deleted Successfully")
    lock.release()
    
