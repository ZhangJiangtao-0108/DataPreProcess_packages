'''
根据特定方法，对emg数据进行校准
'''
import numpy as np

## 计算信息熵
def getEntropy(s):
    s = (np.array(s)+0.0001)     ## 加0.0001的目的是防止nan的出现
    Entropy = np.zeros(s.shape[1])
    for i in range(len(s)):
        Entropy -= np.log2(s[i])*s[i]
    return Entropy

# ## 计算能量
# def getEnergy(s):


## 计算剧烈程度
def getDegree(s):
    Degree = np.zeros(s.shape[1])
    for i in range(len(s)-1):
        Degree += np.abs(s[i+1]-s[i])
    return Degree / (len(s)-1)

def correct(emg_data):
    '''
    功能：对emg数据的数据维度进行校准
    1、将emg信号按照维度进行归一化操作
    2、寻找每个维度的特征：能量，信息熵等
    3、根据每一维的指标对原始的emg信号进行排序
    '''
    emg_data = np.array(emg_data)
    
    ## 按照行对数据进行归一化操作
    max_num = np.max(emg_data,axis=0) 
    min_num = np.min(emg_data,axis=0)
    emg_data_norm = (emg_data - min_num) / (max_num - min_num)
    
    ## 计算每一维的信号熵
    Entropy = getEntropy(emg_data_norm)
    Degree = getDegree(emg_data_norm)
    print('ENTROPY:',Entropy)
    print('DEGREE:',Degree)
    ## 寻找emg_data的维度排序
    sorted_id_Entropy = sorted(range(len(Entropy)), key=lambda k: Entropy[k], reverse=True)
    sorted_id_Degree = sorted(range(len(Entropy)), key=lambda k: Degree[k], reverse=True)
    print('sorted_id_Entropy:',sorted_id_Entropy)
    print('sorted_id_Degree:',sorted_id_Degree)
    
    start_id = sorted_id_Entropy[0]

    ## 寻找排序顺序
    sort_id = [i for i in range(start_id, emg_data.shape[1])] + [i for i in range(0,start_id)]
    ## 将emg_data维数交换顺序

    emg_data = emg_data[:,sort_id]

    return emg_data
    
