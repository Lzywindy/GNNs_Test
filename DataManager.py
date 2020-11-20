import DatasetFiles
from multiprocessing import Process

DatasetFiles.f_disk = 'E:'
DatasetFiles.f_path_fold = 'E:\PeMSD7-2012\原始数据包'
DatasetFiles.f_path_fold_save = 'E:\PeMSD7-2012'
_list = DatasetFiles.GetFiles()
_interval = 8
_index = 0
while _index < len(_list):
    _data_length = min(len(_list) - _index,_interval)
    process_list = list()
    for index in range(_index,_index + _data_length):
        print('File ' + _list[index] + ' in process')
        _process = Process(target=DatasetFiles.Dataset2DataFrame,args=(_list[index],))
        print('Num ' + str(index) + 'has been process created!')
        process_list.append(_process)
        _process.start()
    for item in process_list:
        item.join()
    _index += _data_length