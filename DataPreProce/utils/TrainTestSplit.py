'''
Function: Divide the dataset
Author: ZhangJiangtao-0108
'''

import numpy as np
import random

class TrainTestSplit():
    '''
    
    '''
    def __init__(self, train_size: float=0.8, test_size: float=0.2, shuffle: bool =True):
        self.train_size, self.test_size, self.shuffle = train_size, test_size, shuffle

    def __index_list(self, Data_size):
        index = [i for i in range(Data_size)]
        if self.shuffle:
            self.train_index = random.sample(range(0,Data_size), int(Data_size * self.train_size))
        else:
            self.train_index = [i for i in range(int(Data_size * self.train_size))]
        self.test_index = list(set(index) - set(self.train_index))

    def getIndex(self, Data_size):
        self.__index_list(Data_size)
        return self.train_index, self.test_index

    def split(self, Data, Label):
        self.__index_list(len(Data))
        return Data[self.train_index], Label[self.train_index], Data[self.test_index], Label[self.test_index]

if __name__ == "__main__":
    rs = TrainTestSplit()
    train_index, test_index = rs.getIndex(100)
    print(train_index)
    print(test_index)