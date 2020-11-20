import time

__SID :int
__TimeStamp :float
__TotalFlow :int
__AvgOccup :float
__AvgSpeed :float

class Vertex_Data:
    __TimeStamp :float
    __TotalFlow :int
    __AvgOccup :float
    __AvgSpeed :float
    def __init__(self,TimeStamp,TotalFlow,AvgOccup,AvgSpeed):
        timeArray = time.strptime(TimeStamp, "%m/%d/%Y %H:%M:%S")
        self.TimeStamp = time.mktime(timeArray)
        self.TotalFlow = int(TotalFlow)
        self.AvgOccup = float(AvgOccup)
        self.AvgSpeed = float(AvgSpeed)    
    def __str__(self):
        return str('{Time Stamp:' + str(self.TimeStamp) + ';Total Flow:' + str(self.TotalFlow) + ';Avg Occup:' + str(self.AvgOccup) + ';Avg Speed:' + str(self.AvgSpeed) + '}')
    def toList(self):
        return [__TimeStamp,__TotalFlow,__AvgOccup,__AvgSpeed]

class Vertex_PeMS:
    _total_record_usefuldata = 12
    _SID_local = 1
    _timestamp_local = 0
    _avg_speed_local = _total_record_usefuldata - 1
    _avg_occupancy_local = _total_record_usefuldata - 2
    _total_flow_local = _total_record_usefuldata - 3

    __SID :int
    __Data :Vertex_Data
    def __init__(self,line:str):
        vline = line.split(',',self._total_record_usefuldata)
        vline.remove(vline[self._total_record_usefuldata])
        self.__SID = int(vline[self._SID_local])
        self.__Data = Vertex_Data(vline[self._timestamp_local],vline[self._total_flow_local],vline[self._avg_occupancy_local],vline[self._avg_speed_local])
    def __str__(self):
        return str(self.__SID) + str(self.__Data)


