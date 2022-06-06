import numpy as np

## 数据补全
def Data_Complement(data, dataLen, padding = 0):
    '''
    数据补全：长度超过的直接去除，不够的补齐
        args：
            data：数据
            dataLen：需要填充的形状
            padding：补充的值，默认为0

        return：填充后的数据
    '''
    if dataLen <= len(data):
        return data[:dataLen]
    else:
        return np.append(data, np.full((dataLen-len(data), data.shape[1]), padding), axis=0)

## test
# a = np.ones((120,10))
# b = Data_Complement(a, 100)
# print(b)
# print(b.shape)
