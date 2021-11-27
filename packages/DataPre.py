'''
    数据处理
'''

import numpy as np
import os
from algorithm.cutting_algorithm import cut_data, stretch
from algorithm.Attitude_Angle_solution import data_change
from algorithm.emg_correct import correct
from algorithm.emg_feature import EMGDataFeature

## 数据预处理
class DataPreprocessing():
    def __init__(self, **kwargs) -> None:
        '''进行数据预处理

            args:
                emg: EMG数据
                imu: IMU数据
                isCut: 决定数据是否需要裁切
                isStretch: 决定数据是否需要拉伸
                data_time: 拉伸到data_time时间长度
                isFill: 决定数据是否需要填补
                isIncreEmgDim: 决定EMG数据是否需要扩充维度
        '''
        self.emg = None
        self.imu = None
        self.isCut = kwargs['kwargs'].pop('isCut', False)
        self.isStretch = kwargs['kwargs'].pop('isStretch', False)
        self.data_time = kwargs['kwargs'].pop('data_time', 4)
        self.isFill = kwargs['kwargs'].pop('isFill', False)
        self.isIncreEmgDim = kwargs['kwargs'].pop('isIncreEmgDim', False)

    ## 数据截切
    def DataCut(self, ):
        self.emg, self.imu = cut_data(self.emg, self.imu)
    
    ## 数据拉伸
    def DataStretch(self, ):
        self.emg, self.imu = stretch(self.emg, self.imu, self.data_time)

    ## 数据填充
    def DataFill(self, emg_value = 0,  imu_value = 0):
        emg_line_len = self.data_time * 200
        imu_line_len = self.data_time * 50
        emg_count, imu_count = len(self.emg), len(self.imu)
        ## 处理emg数据
        if emg_count < emg_line_len:
            emg_add = np.array([[emg_value for i in range(8)] for j in range(emg_line_len - emg_count)])
            self.emg = np.vstack([np.array(self.emg), emg_add])
        else:
            self.emg = np.array(self.emg[0:emg_line_len])
        ## 处理imu数据
        if imu_count < imu_line_len:
            imu_add = np.array([[imu_value for i in range(10)] for j in range(imu_line_len - imu_count)])
            self.imu = np.vstack([np.array(self.imu), imu_add])
        else:
            self.imu = np.array(self.imu[0:imu_line_len])

    ## 增加肌电流维数
    def IncreaseEmgDim(self, ):
        Add_Data = self.emg.copy()
        for i in range(len(self.emg[0])-1):
            for j in range(i+1, len(self.emg[0])):
                Add_Data = np.hstack([Add_Data, np.abs(self.emg[:,i] - self.emg[:,j]).reshape(len(self.emg),1)])
        return Add_Data

    ## 肌电流维度矫正
    def CorrectEmgData(self, ):
        self.emg = correct(self.emg)

    ## 数据处理
    def DataPreprocessse(self, emg, imu):
        self.emg, self.imu = emg, imu
        if (not self.emg) or (not self.imu):
            raise ValueError("数据不能为空")
        if self.isCut:
            self.DataCut()
        if self.isStretch:
            self.DataStretch()
        if self.isFill:
            self.DataFill()
        if self.isIncreEmgDim:
            self.emg = self.IncreaseEmgDim()
        
        return np.array(self.emg), np.array(self.imu)

## 提取数据的特征
class ExtractDataFeature():
    def __init__(self, **kwargs) -> None:
        '''进行数据特征提取

            kwargs_pre: 数据预处理参数
                args:
                    isCut: 决定数据是否需要裁切
                    isStretch: 决定数据是否需要拉伸
                    data_time: 拉伸到data_time时间长度
                    isFill: 决定数据是否需要填补
                    isIncreEmgDim: 决定EMG数据是否需要扩充维度
            kwargs_feature: 数据特征提取参数
                args:
                    EMGFeatureType: 提取EMG数据的特征类型，包括：[IEMG, MAV, MAV1, MAV2, SSI, VAR, TM_N, RMS, V, LOG, WL, AAC, DASDV, ZC, MYOP, WAMP, SSC, MAVSLP, MHW, MTW, HIST, HIST, AR, CC]
                    EMGFeatureKwargs: 对应EMG数据特征的参数
                        ZC_threshold: ZC对应的阈值，默认值为0
                        MYOP_threshold: MYOP对应的阈值，默认值为0
                        WAMP_threshold: WAMP对应的阈值，默认值为0
                        SSC_threshold: SSC对应的阈值，默认值为0
                        K: MAVSLP的特征参数，EMG数据对应的分段数，默认值为3
                        N: TM_N对应的阶数
        '''
        self.emg, self.imu = None, None
        kwargs = kwargs['kwargs']
        self.kwargs_pre = kwargs['kwargs_pre']
        self.kwargs_feature = kwargs['kwargs_feature']  
        self.dataPre = DataPreprocessing(kwargs = self.kwargs_pre)

    ## 提取emg信号特征
    def EmgFeature(self, ):
        '''进行EMG数据的特征提取

            args:
                FeatureType: 选择需要的EmgFeature类型，特征类型：[IEMG, MAV, MAV1, MAV2, SSI, VAR, TM_N, RMS, V, LOG, WL, AAC, DASDV, ZC, MYOP, WAMP, SSC, MAVSLP, MHW, MTW, HIST, HIST, AR, CC]
                ZC_threshold: Numerical boundary, The default value of 0.
                MYOP_threshold: Numerical boundary, The default value of 0.
                WAMP_threshold: Numerical boundary, The default value of 0.
                SSC_threshold: Numerical boundary, The default value of 0.
                MAVSLP_K: is number of segments covering the EMG signal, The default value of 3.
                MHW_K: is the size of the hamming windows, the default value is 1
                MTW_K: is the size of the hamming windows, the default value is 1
                N: Order number
                v: is the vorresponding of the feature V, the default value is 1
        '''
        # print(self.kwargs_feature)
        EMGFeatureTypes = self.kwargs_feature['EMGFeatureTypes']
        EMGFeatureKwargs = self.kwargs_feature['EMGFeatureKwargs']
        if ('ZC' in EMGFeatureTypes) and ('ZC_threshold' not in EMGFeatureKwargs):
            return KeyError('The EMGFeatureKwargs don\'t have \"ZC_threshold\" !')
        if ('MYOP' in EMGFeatureTypes) and ('MYOP_threshold' not in EMGFeatureKwargs):
            return KeyError('The EMGFeatureKwargs don\'t have \"MYOP_threshold\" !')
        if ('WAMP' in EMGFeatureTypes) and ('WAMP_threshold' not in EMGFeatureKwargs):
            return KeyError('The EMGFeatureKwargs don\'t have \"WAMP_threshold\" !')
        if ('SSC' in EMGFeatureTypes) and ('SSC_threshold' not in EMGFeatureKwargs):
            return KeyError('The EMGFeatureKwargs don\'t have \"SSC_threshold\" !')
        if ('MAVSLP' in EMGFeatureTypes) and ('K' not in EMGFeatureKwargs):
            return KeyError('The EMGFeatureKwargs don\'t have \"K\" !')
        if ('V' in EMGFeatureTypes) and ('v' not in EMGFeatureKwargs):
            return KeyError('The EMGFeatureKwargs don\'t have \"v\" !')
        if ('MAVSLP' in EMGFeatureTypes) and ('MAVSLP_K' not in EMGFeatureKwargs):
            return KeyError('The EMGFeatureKwargs don\'t have \"MAVSLP_K\" !')
        if ('MHW' in EMGFeatureTypes) and ('MHW_K' not in EMGFeatureKwargs):
            return KeyError('The EMGFeatureKwargs don\'t have \"MHW_K\" !')
        if ('MTW' in EMGFeatureTypes) and ('MTW_K' not in EMGFeatureKwargs):
            return KeyError('The EMGFeatureKwargs don\'t have \"MTW_K\" !')
        if ('TM_N' in EMGFeatureTypes) and ('N' not in EMGFeatureKwargs):
            return KeyError('The EMGFeatureKwargs don\'t have \"N\" !')
        feature_list = []
        feature = EMGDataFeature(self.emg)
        for EMGFeatureType in EMGFeatureTypes:
            feature_list.append(feature.getFeature(EMGFeatureType, kwargs = EMGFeatureKwargs))
        return tuple(feature_list)

    ## 提取imu信号特征
    def ImuFeature(self, ):
        pitch, roll, yaw = data_change(self.imu)
        imu_Euler_angle = []
        for i in range(len(pitch)):
            feature = [0 for i in range(7)]
            feature[0] = self.imu[i][0]
            feature[1] = self.imu[i][1]
            feature[2] = self.imu[i][2]
            feature[3] = self.imu[i][3]
            feature[4] = pitch[i]
            feature[5] = roll[i]
            feature[6] = yaw[i]
            imu_Euler_angle.append(feature)
        
        return np.array(imu_Euler_angle)
    
    ## 整合信号
    def getFeature(self, emg, imu):
        self.emg, self.imu = emg, imu
        if (not self.emg) or (not self.imu):
            raise ValueError("数据不能为空")
        ## 数据预处理
        self.emg, self.imu = self.dataPre.DataPreprocessse(self.emg, self.imu)
        ## 特征提取
        emgFeature = self.EmgFeature()
        imuFeature = self.ImuFeature()

        return emgFeature, imuFeature
        
## 数据提取的生成器
def ReadData(dataPath):
    ## 读取emg数据文件名
    emgDataNames = os.listdir(dataPath + 'emg/')
    for emgDataName in emgDataNames:
        emgDataPath = dataPath + 'emg/' + emgDataName
        imuDataPath = emgDataPath.replace('emg', 'imu')
        # print(emgDataPath)
        # print(imuDataPath)
        ## 读取文件
        emgFile = open(emgDataPath, 'r')
        imuFile = open(imuDataPath, 'r')
        emg = emgFile.read().strip().split('\n')
        for i in range(len(emg)):
            emg[i] = emg[i].strip().split(' ')
            emg[i] = [int(i) for i in emg[i]]
        imu = imuFile.read().strip().split('\n')
        for i in range(len(imu)):
            imu[i] = imu[i].strip().split(' ')
            imu[i] = [float(i) for i in imu[i]]
        ## 关闭文件
        emgFile.close()
        imuFile.close()
        ## 生成label
        label = emgDataName.split('_')[0].split('-')
        ## 生成志愿者
        scale = emgDataName.split('_')[1]
        yield emg, imu, label, scale

## 数据处理生成器
def dataGenerator(dataPath, kwargs):
    data = ReadData(dataPath)
    # print(kwargs)
    # dataPre = DataPreprocessing(kwargs = kwargs)
    dataFeatureExtract = ExtractDataFeature(kwargs = kwargs)
    while True:
        try:
            emg, imu, label, scale = next(data)
            # emg_pre, imu_pre = dataPre.DataPreprocessse(emg, imu)
            # yield np.array(emg_pre), np.array(imu_pre), label, scale
            emg_feature, imu_feature = dataFeatureExtract.getFeature(emg, imu)
            yield np.array(emg_feature), np.array(imu_feature), label, scale
        except StopIteration:
            return

if __name__ == '__main__':

    dataPath = r'C:/Users/张江涛/Desktop/imu测试/imu_sentence数据/'
    kwargs = {'isCut':True,
              'isStretch':False,
              'isFill':True,
              'data_time':6,
              'isIncreEmgDim':True}
    data = iter(dataGenerator(dataPath, kwargs))
    for emg, imu, label, scale in data:
        print(emg.shape)
        print(imu.shape)
    #     pass
        # i += 1
        # print(i)
    # emg, imu = next(data)
    # print(emg.shape)
    # print(imu.shape)
    # emg, imu = next(data)
    # print(emg.shape)
    # print(imu.shape)

