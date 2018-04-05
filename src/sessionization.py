
"""
Author: Susie Huang

Solution:
This program reads through the input file (log.csv) line by line using the 
headers to determine the fields, creates or updates the session objects and 
stores sessionized data in a nested dictionary with IP address as the key 
(unique identifier for each user). 

"""


# Import module
import datetime
import operator
import csv
import sys


# Define the session timeout function for export. As long as the session meets all session closing rules, export to the output file in an order and delete them from the dictionary simultaneously.
def export_timeout_session(myDict, timestamp, session_timeout, outfile):
    to_be_deleted_list= []
    for key,value in myDict.items():
        if timestamp > value['last_seen'] + datetime.timedelta(seconds=session_timeout):
            to_be_deleted_list.append((key,value['line_num']))
            sorted(to_be_deleted_list, key=lambda x: x[1])  # Sorted by the original order appears in the input file
    for (key,line_num) in to_be_deleted_list:
        value = myDict[key]
        duration = (value['last_seen']-value['start_time']+ datetime.timedelta(seconds=1)).total_seconds()
        outfile.write("%s,%s,%s,%d,%d\n" % (key,value['start_time'],value['last_seen'],duration,value['doc_ct']))
        del myDict[key]

def main():

    # Set up terminal arguments
    infileName = sys.argv[1]
    sessiontimeoutfileName = sys.argv[2]
    outfileName =  sys.argv[3]

    # Load input, output and inactivity files
    outfile = open(outfileName, "w")
    session_timeout_file = open(sessiontimeoutfileName,'r')
    session_timeout = int(session_timeout_file.read())
    infile = open(infileName, 'r')

    # Set up header index, using the headers to determine the fields instead of the order of the fields
    f = csv.reader(infile)
    header = next(f)
    ipIndex = header.index("ip")
    dateIndex = header.index("date")
    timeIndex = header.index("time")
    
    ipDict = {} # Create a dictionary indexed by IP
    
    line_num = 1 # Create line number counter to record the original order of input file before export
    
    for line in infile:
        fields = line.split(',')
        ip = fields[ipIndex]
        date = fields[dateIndex]
        time = fields[timeIndex]
        doc_ct = 1
        # Use datetime module to convert into a timestamp format
        timestamp = datetime.datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S")
        
        # Scan the dictionary and close the session. 
        ## Execute the session closing and export function once the latest activity time shows inactivity time has elapsed
        export_timeout_session(ipDict, timestamp, session_timeout, outfile)
        
        # For the rest in the dictionary whose session not yet time out.
        ## If this is the first request of an IP, create the sessions object and append it to the bottom of the dictionary. 
        if ip not in ipDict:
            ipDict[ip] = {'line_num': line_num, 'start_time':timestamp, 'last_seen':timestamp,'doc_ct':doc_ct}

        ## If this IP's session already exists, update its latest activity time ('last_seen') and number of document requests ('doc_ct'). 
        else:
            ipDict[ip]['doc_ct'] += 1
            ipDict[ip]['last_seen'] = timestamp
        
        line_num += 1
    

    # When the end of file has been reached (exit the for loop above), close and export all remaining sessions by executing the session closing and export function previously defined
    export_timeout_session(ipDict, timestamp, -1, outfile)

    outfile.close()
    infile.close()
    session_timeout_file.close()

if __name__ == "__main__":
    main()
