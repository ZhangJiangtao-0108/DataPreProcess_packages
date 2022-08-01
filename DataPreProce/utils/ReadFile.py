'''
    Read EMG or IMU file data and return 2D data in the corresponding format
'''

import os
import numpy as np



def ReadFile(DataPath, DataType = "int"):
    '''
        DataPath:数据路径
        DataType:返回的数据类型
    '''
    DataFile = open(DataPath, 'r')
    data = []
    for line in DataFile.readlines():
        line = line.replace("\n", '').split(' ')
        lin = [eval(DataType)(k) for k in line]
        data.append(lin)
    DataFile.close()
    data = np.array(data)

    return data