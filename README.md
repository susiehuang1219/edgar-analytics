# Introduction

This program is a solution to Insight Data Engineering Code Challenge. The objective of this challenge is to build a pipeline to ingest and sessionize the stream of SEC weblogs data in order to calculate how long a particular user spends on EDGAR during a visit and how many documents that user requests during the session. The code runs on Python 3.6. It reads through the input file (log.csv) line by line using the headers to determine the fields, creates or updates the session object and stores sessionized data in a nested dictionary with IP address as the key (unique identifier for each user). 


## Session timeout/closing rule
This program defines a session timeout and export function based on the inactivity. Once the latest activity time shows inactivity time has elapsed, session IP appends to a list to be sorted by the order of the input file and deletes from the dictionary after exporting closed sessions to the output file. If the end of the file has been reached but still some remaining sessions in the dictionary not yet expired, the same session timeout/export function will be executed, just without checking the inactivity (set inactivity = -1). 


## Create and update sessions in the dictionary
For the sessions not yet time out: if this is the first request of an IP, create the session content and add it to the dictionary; if this IP's session already exists, update its latest activity time ('last_seen') and number of document requests ('doc_ct').

## Order for output file
It creates a line number counter into the dictionary when reading through the input files line by line, which can record the original order of input file. If there are multiple user sessions ending at the same time, it should write the results to the output file in the same order as the user's first request for that session appeared in the input file.

## Miscellaneous

### Read input file by headers: 
It uses the headers (create header index) to determine which fields to read, instead of the order of the fields. 

### Convert date and time: 
It uses python's datetime module to easily manipulate dates/times format and compute duration.

# Space and time complexity

Using a dictionary has O(1) complexity for adding and updating sessions in the dictionary and O(n) to find timeout sessions within the dictionary. The current dictionary solution is fast, only took <3 seconds to complete 1 hour of the real SEC weblog data in my testing. If there are a lot of ongoing sessions, it has to go through the entire dictionary each time. A better approach for such scenario would be using heap, which only needs to compare the top of the heap but that could make the code much more complex. 

# Test process

Three different test cases with pre-defined input and output files have been placed in insight_testsuite/tests. The first one is the original test case provided in the code challenge, the second one has random order of input file and the third one has many sessions not yet closed when end of file is reached. Each test case has different inactivity (timeout) time and focus on different aspects in the code solution. All three test cases have been passed successfully. 


