# -*- coding:utf-8 -*-
'''
name:切割数据的算法
writer:zjt
version:1.0
'''

import math
import numpy as np

'''
增加肌电流维数
'''
def IncreaseEmgDim(emg_data):
    '''
    在EMG信号中，对任意两维数信号进行组合，变成新的一维数据，变形结束后一共28维数
    操作：取两维数据差值的绝对值
    emg_data = [T, dim] --> [T, dim*(dim-1)/2]
    '''
    Add_Data = emg_data.copy()
    for i in range(len(emg_data[0])-1):
        for j in range(i+1, len(emg_data[0])):
            # print(Add_Data.shape)
            # print(np.abs(emg_data[:,i] -emg_data[:,j]).reshape(len(emg_data),1).shape)
            Add_Data = np.hstack([Add_Data, np.abs(emg_data[:,i] - emg_data[:,j]).reshape(len(emg_data),1)])
            # print(Add_Data)
    
    return Add_Data



'''
寻找切割点
'''
def Interpolation(data):
    '''
    寻找前后信号的距离，返回距离列表
    :param data:
    :return:
    '''
    inter = []
    for i in range(len(data)):
        sum = 0
        for j in range(len(data[i])-1):
            sum = pow(data[i][j+1]-data[i][j],2)
        inter.append(math.sqrt(sum))
    return inter

def segmentation_point(data,d):
    '''
    寻找分割点，参数d是阀值，emg和imu的阀值不一致
    :param data:
    :return:
    '''
    inter = Interpolation(data)
    start = 0.0
    end = float(len(data)/len(data))
    for i in range(len(inter)-1):
        if int(inter[i+1] - inter[i]) > d:
            start = i/len(data)
            break
        else:
            continue
    # print("start:",start)
    for j in range(1,len(inter)):
        if int(inter[len(inter)-j] - inter[len(inter)-j-1]) > d:
            end = (len(inter)-j+1)/len(data)
            break
        else:
            continue
    # print("end:",end)
    return start,end

def cut_data(emg_data,imu_data):
    '''
    确定切割点，并切割信号
    :param data:
    :return:
    '''
    start1,end1 = segmentation_point(emg_data,3)
    start2,end2 = segmentation_point(imu_data,4)
    start = min(start1,start2)
    end = max(end1,end2)
    emg_start, emg_end = int(start * len(emg_data)), int(end * len(emg_data))
    imu_start, imu_end = int(start * len(imu_data)), int(end * len(imu_data))
    # print(emg_start, emg_end)
    # print(imu_start, imu_end)
    return emg_data[emg_start:emg_end], imu_data[imu_start:imu_end]

def stretch(emg_data,imu_data,data_time):
    '''
    将切割出来的信号转换成为统一长度，长的缩短，短的伸长。
    :param emg_data:
    :param imu_data:
    :return:
    '''
    emg_data = list(emg_data)
    imu_data = list(imu_data)  
    emg_len = data_time * 200   # 定义emg数据的长度
    imu_len = data_time * 50   # 定义imu数据的长度
    if len(emg_data) <= emg_len:
        '''
        将emg信号伸长，在确定的位置处添加数据
        '''
        emg_difference = emg_len - len(emg_data)
        if emg_difference > 0:
            emg_step = len(emg_data) / emg_difference
            for i in range(emg_difference):
                temp = []
                for j in range(8):
                    temp.append((emg_data[int(emg_step*(emg_difference-i))-2][j] + emg_data[int(emg_step*(emg_difference-i))-1][j])/2)
                emg_data.insert(int(emg_step*(emg_difference-i))-1,temp)
        else:
            emg_data = emg_data
    else:
        '''
        将emg数据缩短，在确定位置处删除数据
        '''
        emg_difference = len(emg_data) - emg_len
        emg_step = len(emg_data) / emg_difference
        for i in range(emg_difference):
            del emg_data[int(emg_step*(emg_difference-i))-1]


    if len(imu_data) <= imu_len:
        '''
        将imu信号伸长，在确定的位置处添加数据
        '''
        imu_difference = imu_len - len(imu_data)
        if imu_difference > 0:
            imu_step = len(imu_data) / imu_difference
            for i in range(imu_difference):
                temp = []
                for j in range(10):
                    temp.append((imu_data[int(imu_step*(imu_difference-i))-2][j] + imu_data[int(imu_step*(imu_difference-i))-1][j])/2)
                imu_data.insert(int(imu_step*(imu_difference-i))-1,temp)
        else:
            imu_data = imu_data
    else:
        '''
        将imu数据缩短，在确定位置处删除数据
        '''
        imu_difference = len(imu_data) - imu_len
        imu_step = len(imu_data) / imu_difference
        for i in range(imu_difference):
            del imu_data[int(imu_step*(imu_difference-i))-1]

    return np.array(emg_data), np.array(imu_data)

class Stretch():
    '''
    
    '''
    def __init__(self, data_time):
        self.emg_len = data_time * 200
        self.imu_len = data_time * 50

    def stretch(self, emg_data, imu_data, Segment:bool=None):
        '''
        将切割出来的信号转换成为统一长度，长的缩短，短的伸长。
        :param emg_data:
        :param imu_data:
        :return:
        '''
        emg_data = list(emg_data)
        imu_data = list(imu_data)  
        if Segment:
            emg_len, imu_len = self.emg_len / 10, self.imu_len / 10
        else:
            emg_len, imu_len = self.emg_len, self.imu_len
        if len(emg_data) <= emg_len:
            '''
            将emg信号伸长，在确定的位置处添加数据
            '''
            emg_difference = emg_len - len(emg_data)
            if emg_difference > 0:
                emg_step = len(emg_data) / emg_difference
                for i in range(emg_difference):
                    temp = []
                    for j in range(8):
                        temp.append((emg_data[int(emg_step*(emg_difference-i))-2][j] + emg_data[int(emg_step*(emg_difference-i))-1][j])/2)
                    emg_data.insert(int(emg_step*(emg_difference-i))-1,temp)
            else:
                emg_data = emg_data
        else:
            '''
            将emg数据缩短，在确定位置处删除数据
            '''
            emg_difference = len(emg_data) - emg_len
            emg_step = len(emg_data) / emg_difference
            for i in range(emg_difference):
                del emg_data[int(emg_step*(emg_difference-i))-1]


        if len(imu_data) <= imu_len:
            '''
            将imu信号伸长，在确定的位置处添加数据
            '''
            imu_difference = imu_len - len(imu_data)
            if imu_difference > 0:
                imu_step = len(imu_data) / imu_difference
                for i in range(imu_difference):
                    temp = []
                    for j in range(10):
                        temp.append((imu_data[int(imu_step*(imu_difference-i))-2][j] + imu_data[int(imu_step*(imu_difference-i))-1][j])/2)
                    imu_data.insert(int(imu_step*(imu_difference-i))-1,temp)
            else:
                imu_data = imu_data
        else:
            '''
            将imu数据缩短，在确定位置处删除数据
            '''
            imu_difference = len(imu_data) - imu_len
            imu_step = len(imu_data) / imu_difference
            for i in range(imu_difference):
                del imu_data[int(imu_step*(imu_difference-i))-1]

        return np.array(emg_data), np.array(imu_data)

    def segment_stretch(self, emg_data, imu_data):
        '''
        
        '''
        emg_shape = emg_data.shape
        imu_shape = imu_data.shape
        emg_shape[0] = self.emg_len
        imu_shape[0] = self.imu_len
        emg = np.zeros(emg_shape)
        imu = np.zeros(imu_shape)
        emg_step = self.emg_len / 10
        imu_step = self.imu_len / 10
        emg_segment_len = int(len(emg_data) / 10)
        imu_segment_len = int(len(imu_data) / 10)

        for i in range(9):
            emg[i*emg_step:(i+1)*emg_step], imu[i*imu_step:(i+1)*imu_step] = self.stretch(emg_data[i * emg_segment_len: (i+1) * emg_segment_len], imu_data[i * imu_segment_len: (i+1) * imu_segment_len], Segment= True) 
        emg[9*emg_step:], imu[9*imu_step:] = self.stretch(emg_data[9 * emg_segment_len:], imu_data[9 * imu_segment_len:], Segment= True)
        return emg, imu

