# README

This project aims to modify nested dictionaries. Motivation for this is the  
output of MongoDb, where dates are returned as e.g. 

`{'date' : { '$date' : '2021-01-01 12:13:14'}}`

and the desired output is 

`{'date' : '2021-01-01 12:13:14'}`

There are two main functionalities: 

## Reduce key, value to value (method nested_change)

This library detects keys within a nested dictionary and transforms 
the `{ key : value }` pair to `value`. 

## Transform dict to csv list (method dict2list)

The dictionary is traversed and all entries are transformed into 
a csv-like list of a `key; value` with key being a combination of 
all nested keys of the element and value is the actual value. 



