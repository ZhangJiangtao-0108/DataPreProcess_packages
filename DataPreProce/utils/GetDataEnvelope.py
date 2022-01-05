"""
    求某一维度的包络信号
"""

def getDataEnvelope(data):
    '''
        只求某一维度的包络信号

        args:
            data:一维数据

        return：
            data_envelope:数据的包络信号
            index:包络信号在原数据中的索引
    '''
    data_envelope = []
    index_ = []
    for i in range(len(data)-1):
        if data[i] - data[i-1] > 0 and data[i+1] - data[i] < 0:
            index_.append(i)
            data_envelope.append(data[i])
    
    return np.array(data_envelope), np.array(index_)

