import numpy as np
from scipy import sparse as sp

#得到内容函数(读出来为行存储模式)
def GetContext(filename:str):
    '''
        得到文件内容
        :filename: 文件的全路径, str
        :result: 文件内容，被划分为行形式
    '''
    f = open(filename)
    try:
        #content = f.read()
        lines = f.readlines()
    finally:
        f.close()
    #lines = content.split('\n')
    lines = [inf for inf in lines if inf != '']
    return lines
def _GetDataNodes(lines:list,lables_convert:dict):
    labled_x = []
    labled_y = []
    labled_list_id = {}
    nonlabled_x = []
    nonlabled_y = []
    nonlabled_list_id = {}
    labled_count = 0
    nonlabled_count = 0
    for line in lines:
        sp_line = line.split()
        length = len(sp_line)
        if(sp_line[length - 1] in lables_convert.keys()):
            if(sp_line[0] in labled_list_id.keys()):
                continue
            labled_list_id[sp_line[0]] = labled_count
            labled_count+=1
            labled_x.append(list(map(int,sp_line[1:length - 2])))
            labled_y.append(lables_convert[sp_line[length - 1]])
        else:
            if(sp_line[0] in nonlabled_list_id.keys()):
                continue
            nonlabled_list_id[sp_line[0]] = nonlabled_count
            nonlabled_count+=1
            nonlabled_x.append(list(map(int,sp_line[1:length - 2])))
            nonlabled_y.append(lables_convert['default'])
    return tuple([np.asarray(labled_x,dtype= float),np.asarray(labled_y,dtype= float),labled_list_id,np.asarray(nonlabled_x,dtype= float),np.asarray(nonlabled_y,dtype= float),nonlabled_list_id])
def _GetDataNodes_NS(lines:list,lables_convert:dict):
    labled_x = []
    labled_y = []
    labled_list_id = {}
    labled_count = 0
    for line in lines:
        sp_line = line.split()
        length = len(sp_line)
        if(sp_line[0] in labled_list_id.keys()):
            continue
        labled_list_id[sp_line[0]] = labled_count
        labled_count+=1
        labled_x.append(list(map(int,sp_line[1:length - 2])))
        if(sp_line[length - 1] in lables_convert.keys()):
            labled_y.append(lables_convert[sp_line[length - 1]])
        else:
            labled_y.append(lables_convert['default'])
    return tuple([np.asarray(labled_x,dtype= float),np.asarray(labled_y,dtype= float),labled_list_id])
def _GetAdjacencyMatrix(lines:list,list_id:dict):
    if(len(list_id) == 0):
        return None
    adj_matrix = np.zeros([len(list_id),len(list_id)],dtype=float)
    for line in lines:
         sp_line = line.split()
         if(sp_line[0] not in list_id.keys() or sp_line[1] not in list_id.keys()):
             continue
         adj_matrix[list_id[sp_line[0]],list_id[sp_line[1]]] = 1
    return adj_matrix
def _GetPubmedLabRange(lable:str):
    lable_type = lable.split(':')
    return tuple([lable_type[1],list(map(int,lable_type[0].split('=')[1].split(',')))])
def _GetPubmedFeatures(lable:str):
    features = lable.split(':')
    defaultvalue = 0
    if(features[0] == 'numeric' and len(features) == 3):
        defaultvalue = float(features[2])
    elif(features[0] == 'numeric' and len(features) < 3):
        defaultvalue = 0
    elif(features[0] == 'summary' and len(features) == 3):
        defaultvalue = features[2]
    else:
        defaultvalue = ''
    return tuple([features[1],defaultvalue])
def _GetPubmedTags(line_elements:str):
    elements = line_elements.split()
    dict_default_value = {}
    dict_index = {}
    length = len(elements)
    count = -1
    for index in range(0,length,1):
        if(index == 0):
            tag,value = _GetPubmedLabRange(elements[index])
        else:
            tag,value = _GetPubmedFeatures(elements[index])
        dict_default_value[tag] = value
        dict_index[tag] = count
        count+=1
    return tuple([dict_index,dict_default_value])
def _GetPubmedDataLabs(lines:list,index:dict,lables_convert:dict):
    dict_index_row = {}
    lables = []
    nodes = []
    count = 0
    for line in lines:
        elements = line.split()
        length = len(elements)
        lable = []
        node = [0 for i in range(1,len(index) - 1)]
        for _index in range(1,length ,1):
            data = elements[_index].split('=')
            if(data[0] == 'summary'):
                continue
            if(index[data[0]] == -1):
                if(int(data[1]) in lables_convert.keys()):
                    lable = lables_convert[int(data[1])]
                else:
                    lable = lables_convert[0]
            else:
                node[index[data[0]]] = float(data[1])
        lables.append(lable)
        nodes.append(node)
        dict_index_row[elements[0]] = count
        count+=1
    return tuple([sp.csc_matrix(nodes), sp.csc_matrix(lables),dict_index_row])
def _Get_Terror_Atk(path:str):
    _path = path + "terrorist-attacks\\"
    lables_convert = {'http://counterterror.mindswap.org/2005/terrorism.owl#Arson':[1,0,0,0,0,0],'http://counterterror.mindswap.org/2005/terrorism.owl#Bombing':[0,1,0,0,0,0],'http://counterterror.mindswap.org/2005/terrorism.owl#Kidnapping':[0,0,1,0,0,0],'http://counterterror.mindswap.org/2005/terrorism.owl#NBCR_Attack':[0,0,0,1,0,0],'http://counterterror.mindswap.org/2005/terrorism.owl#other_attack':[0,0,0,0,1,0],'http://counterterror.mindswap.org/2005/terrorism.owl#Weapon_Attack':[0,0,0,0,0,1],'default':[0,0,0,0,0,0]}
    xl,yl, list_id_l,xul,yul, list_id_ul = _GetDataNodes(GetContext(_path + 'terrorist_attack.nodes'),lables_convert)
    return [sp.csr_matrix(xl),sp.csr_matrix(yl),sp.csr_matrix(_GetAdjacencyMatrix(GetContext(_path + 'terrorist_attack_loc.edges'),list_id_l)),sp.csr_matrix(_GetAdjacencyMatrix(GetContext(_path + 'terrorist_attack_loc_org.edges'),list_id_l))]
def _Get_Terror_Rel(path:str):
    _path = path + "terrorists-relay\\"
    lables_convert = {'contact':[1,0,0,0],'family':[0,1,0,0],'colleague':[0,0,1,0],'congregate':[0,0,0,1],'default':[0,0,0,0]}
    datafilenm = ['TerroristRel_Colleague','TerroristRel_Congregate','TerroristRel_Contact','TerroristRel_Family']
    dict_Terror_Rel_Set = {}
    for nm in datafilenm:
        xl,yl, list_id_l = _GetDataNodes_NS(GetContext(_path + nm + '.nodes'),lables_convert)  
        dict_Terror_Rel_Set[nm] = [sp.csr_matrix(xl),sp.csr_matrix(yl),list_id_l,sp.csr_matrix(_GetAdjacencyMatrix(GetContext(_path + 'TerroristRel.edges'),list_id_l))]
    return dict_Terror_Rel_Set
def Get_Citeseer_DataSet(path:str):
    lables_convert = {'Agents':[1,0,0,0,0,0],'AI':[0,1,0,0,0,0],'DB':[0,0,1,0,0,0],'IR':[0,0,0,1,0,0],'ML':[0,0,0,0,1,0],'HCI':[0,0,0,0,0,1],'default':[0,0,0,0,0,0]}
    xl,yl, list_id_l = _GetDataNodes_NS(GetContext(path + 'citeseer.content'),lables_convert)       
    adj_matrix = _GetAdjacencyMatrix(GetContext(path + 'citeseer.cites'),list_id_l)
    return [sp.csr_matrix(xl),sp.csr_matrix(yl),sp.csr_matrix(adj_matrix),list_id_l]
def Get_Cora_DataSet(path:str):
    lables_convert = {'Case_Based':[1,0,0,0,0,0,0],'Genetic_Algorithms':[0,1,0,0,0,0,0],'Neural_Networks':[0,0,1,0,0,0,0],'Probabilistic_Methods':[0,0,0,1,0,0,0],'Reinforcement_Learning':[0,0,0,0,1,0,0],'Rule_Learning':[0,0,0,0,0,1,0],'Theory':[0,0,0,0,0,0,1],'default':[0,0,0,0,0,0,0]}
    xl,yl, list_id_l = _GetDataNodes_NS(GetContext(path + 'cora.content'),lables_convert)       
    adj_matrix = _GetAdjacencyMatrix(GetContext(path + 'cora.cites'),list_id_l)
    return [sp.csr_matrix(xl),sp.csr_matrix(yl),sp.csr_matrix(adj_matrix),list_id_l]
def Get_PubmedDataSet(path:str):
    lines = GetContext(path + 'data\\Pubmed-Diabetes.NODE.paper.tab')
    lables_convert = {1:[1,0,0],2:[0,1,0],3:[0,0,1],0:[0,0,0]}
    index,default_value = _GetPubmedTags(lines[1])
    nodes,lables,dict_index_row = _GetPubmedDataLabs(lines[2:],index,lables_convert)
    adj_matrix = np.zeros([len(dict_index_row),len(dict_index_row)],dtype=float)
    lines = GetContext(path + 'data\\Pubmed-Diabetes.DIRECTED.cites.tab')[2:]
    for line in lines:
        elements = line.replace('|','').replace('paper:','').split()
        if(elements[1] in dict_index_row.keys() and elements[2] in dict_index_row.keys()):
            adj_matrix[dict_index_row[elements[1]],dict_index_row[elements[2]]] = 1
    return [nodes,lables,sp.csr_matrix(adj_matrix),dict_index_row]
def Get_WebKB_DataSet(path:str):
    lables_convert = {'course':[1,0,0,0,0],'faculty':[0,1,0,0,0],'student':[0,0,1,0,0],'project':[0,0,0,1,0],'staff':[0,0,0,0,1],'default':[0,0,0,0,0]}
    datafilenm = ['cornell','texas','washington','wisconsin']
    dict_WebKB_Set = {}
    for nm in datafilenm:
        xl,yl, list_id_l = _GetDataNodes_NS(GetContext(path + nm + '.content'),lables_convert)  
        adj_matrix = _GetAdjacencyMatrix(GetContext(path + nm + '.cites'),list_id_l)
        dict_WebKB_Set[nm] = [sp.csr_matrix(xl),sp.csr_matrix(yl),sp.csr_matrix(adj_matrix),list_id_l]
    return dict_WebKB_Set
def Get_Terror_DataSet(path:str):
    return {'terrorist-attacks':_Get_Terror_Atk(path),'terrorists-relay':_Get_Terror_Rel(path)}


