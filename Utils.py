import time

total_record_usefuldata = 12
SID_local = 1
timestamp_local = 0
avg_speed_local = total_record_usefuldata - 1
avg_occupancy_local = total_record_usefuldata - 2
total_flow_local = total_record_usefuldata - 3

def SpiltData2List(line:str):
    line = line.split(',',total_record_usefuldata)
    timeArray = time.strptime(line[timestamp_local], "%m/%d/%Y %H:%M:%S")
    if line[total_flow_local] == '':
        t_0 = 0
    else:
        t_0 = int(line[total_flow_local])
    if line[avg_occupancy_local] == '':
        t_1 = 0
    else:
        t_1 = float(line[avg_occupancy_local])
    if line[avg_speed_local] == '':
        t_2 = 0
    else:
        t_2 = float(line[avg_speed_local])
    return [int(line[SID_local]),time.mktime(timeArray),[t_0,t_1,t_2]]

def addtwodimdict(thedict:dict, key_a, key_b, val):
    if key_a in thedict:
        thedict[key_a].setdefault(key_b,val)
    else:
        thedict.setdefault(key_a,{key_b,val})
