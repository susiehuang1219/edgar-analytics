import datetime
import operator
import csv
import sys

def export_timeout_session(myDict, timestamp, session_timeout, outfile):
    to_be_deleted_list= []
    for key,value in myDict.items():
        if timestamp > value['last_seen'] + datetime.timedelta(seconds=session_timeout):
            to_be_deleted_list.append((key,value['line_num']))
            sorted(to_be_deleted_list, key=lambda x: x[1])
    for (key,line_num) in to_be_deleted_list:
        value = myDict[key]
        duration = (value['last_seen']-value['start_time']+ datetime.timedelta(seconds=1)).total_seconds()
        outfile.write("%s,%s,%s,%d,%d\n" % (key,value['start_time'],value['last_seen'],duration,value['doc_ct']))
        del myDict[key]

def main():
    infileName = sys.argv[1]
    sessiontimeoutfileName = sys.argv[2]
    outfileName =  sys.argv[3]


    outfile = open(outfileName, "w")
    session_timeout_file = open(sessiontimeoutfileName,'r')
    session_timeout = int(session_timeout_file.read())

    infile = open(infileName, 'r')
    f= csv.reader(infile)
    header = next(f)
    ipIndex = header.index("ip")
    dateIndex = header.index("date")
    timeIndex = header.index("time")

    ipDict = {}
    
    line_num = 1
    
    for line in infile:
        fields = line.split(',')
        ip = fields[ipIndex]
        date = fields[dateIndex]
        time = fields[timeIndex]
        doc_ct = 1
        timestamp = datetime.datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S")
        
        export_timeout_session(ipDict, timestamp, session_timeout, outfile)

        if ip not in ipDict:
            ipDict[ip] = {'line_num': line_num, 'start_time':timestamp, 'last_seen':timestamp,'doc_ct':doc_ct}
        else:
            ipDict[ip]['doc_ct']+=1
            ipDict[ip]['last_seen'] = timestamp
        line_num += 1

    export_timeout_session(ipDict, timestamp, -1, outfile)

    outfile.close()
    infile.close()
    session_timeout_file.close()

if __name__ == "__main__":
    main()
