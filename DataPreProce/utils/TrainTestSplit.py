'''
Function: Divide the dataset
Author: ZhangJiangtao-0108
'''

import numpy as np
import random

class TrainTestSplit():
    '''
    划分数据集，可以返回数据分割后的标签，也可以返回分割好的数据
    '''
    def __init__(self, train_size: float=0.8, test_size: float=0.1, val_size:float=0.1, val: bool=False, shuffle: bool =True):
        self.train_size, self.test_size, self.val_size, self.val, self.shuffle = train_size, test_size, val_size, val, shuffle
            

    def __index_list(self, Data_size):
        index = np.array([i for i in range(Data_size)])
        if self.shuffle:
            np.random.shuffle(index)
            # self.train_index = random.sample(range(0,Data_size), int(Data_size * self.train_size))
            # self.train_index = [i for i in range(int(Data_size * self.train_size))]
        # self.test_index = list(set(index) - set(self.train_index))
        self.train_index = index[0:int(Data_size * self.train_size)]
        self.test_index = index[int(Data_size * self.train_size):int(Data_size * self.train_size) + int(Data_size * self.test_size)]
        if self.val:
            self.val_index = index[int(Data_size * self.train_size) + int(Data_size * self.test_size):-1]

    def getIndex(self, Data_size):
        self.__index_list(Data_size)
        if self.val:
             return self.train_index, self.val_index, self.test_index
        else:
            return self.train_index, self.test_index

    def split(self, Data, Label):
        self.__index_list(len(Data))
        if self.val:
            return Data[self.train_index], Label[self.train_index], Data[self.val_index], Label[self.val_index], Data[self.test_index], Label[self.test_index]
        else:
            return Data[self.train_index], Label[self.train_index], Data[self.test_index], Label[self.test_index]

if __name__ == "__main__":
    rs = TrainTestSplit(val=True)
    train_index, val_index, test_index = rs.getIndex(100)
    print(train_index)
    print(val_index)
    print(test_index)