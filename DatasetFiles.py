import os
import time
import threading
import pandas as pd

f_disk = r'I:'
f_path_fold = f_disk + r'\PeMSD7-2012原始数据集\原始数据包PeMSD72012HY'
f_path_fold_save = f_disk + r'\PeMSD7-2012原始数据集'
__f_file_source_name_start = r'd07_text_station_5min_'
__f_file_source_expand = '.txt'

def GetFiles():
    files = os.listdir(f_path_fold)
    files = [file for file in files if file.startswith(__f_file_source_name_start) and file.endswith(__f_file_source_expand)]
    return files

def GetContext(filename:str):
    f = open(f_path_fold + '\\' + filename)
    try:
        content = f.read()
    finally:
        f.close()
    lines = content.split('\n')
    lines = [inf for inf in lines if inf != '']
    return lines

__total_record_usefuldata = 12
__SID_local = 1
__timestamp_local = 0
__avg_speed_local = __total_record_usefuldata - 1
__avg_occupancy_local = __total_record_usefuldata - 2
__total_flow_local = __total_record_usefuldata - 3

def SpiltData2List(line:str):
    line = line.split(',',__total_record_usefuldata)
    timeArray = time.strptime(line[__timestamp_local], "%m/%d/%Y %H:%M:%S")
    if line[__total_flow_local] == '':
        t_0 = 0
    else:
        t_0 = int(line[__total_flow_local])
    if line[__avg_occupancy_local] == '':
        t_1 = 0
    else:
        t_1 = float(line[__avg_occupancy_local])
    if line[__avg_speed_local] == '':
        t_2 = 0
    else:
        t_2 = float(line[__avg_speed_local])
    return [int(line[__SID_local]),time.mktime(timeArray),[t_0,t_1,t_2]]

def Dataset2DataFrame(filename:str):
    array_row = list()
    array_col = list()
    array_data = list()
    list_thread = list()
    name = filename.replace('.txt','')
    print('File Process: ' + name + ' started...')
    lines = GetContext(filename)
    for line in lines:
        data = SpiltData2List(line)
        if data[1] not in array_row:
            array_row.append(data[1])
        if data[0] not in array_col:
            array_col.append(data[0])
        array_data.append(data)
    print('Select Datas Complete!')
    df = pd.DataFrame(data=None,index=array_row,columns=array_col)
    array_thread = list()
    for item in array_data:   
        thread = threading.Thread(target=thread_fun,args=(item,))
        array_thread.append(thread)
        thread.start()
    for t in array_thread:
        t.join()
    print(name + ':Datas to Arrays Complete!')
    df.to_pickle(DatasetFiles.f_path_fold_save + '\\' + name + '.pkl')
    print(name + 'Data Save Complete!')
    print('Total Row:' + str(len(array_row)))
    print('Total Col:' + str(len(array_col)))
    print('Total Data:' + str(len(array_data)))





