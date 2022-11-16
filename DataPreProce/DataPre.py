'''
    数据处理
'''
import imp
import numpy as np
import operator
import os
from scipy.fftpack import fft,ifft
import sys
from algorithm.cutting_algorithm import cut_data, Stretch
from algorithm.Attitude_Angle_solution import data_change
from algorithm.emg_correct import correct
from algorithm.emg_feature import EMGDataFeature
from algorithm.imu_feature import IMUDataFeature
from algorithm.Butter_filter import butter_filter, Wave_filter
from algorithm.Data_Complement import Data_Complement
from utils.ReadFile import ReadFile

## 数据预处理
class DataPreprocessing():
    def __init__(self, **kwargs) -> None:
        '''进行数据预处理
            kwargs：
                kwargs_pre：
                    emg：EMG数据
                    imu:：IMU数据
                    emg_F：EMG数据的频域处理信息
                    segment：决定数据的裁剪段数
                    emgChannel：选择emg数据的通道
        '''
        self.emg = None
        self.imu = None
        self.emg_F = None
        self.isCut = kwargs['kwargs_pre'].get('isCut', False)
        self.isStretch = kwargs['kwargs_pre'].get('isStretch', False)
        self.data_time = kwargs['kwargs_pre'].get('data_time', 4)
        self.isFill = kwargs['kwargs_pre'].get('isFill', False)
        self.isFilter = kwargs['kwargs_pre'].get('isFilter', False)
        if self.isFilter:
            self.Filter_args = kwargs['kwargs_pre'].get('Filter_args')
        self.isIncreEmgDim = kwargs['kwargs_pre'].get('isIncreEmgDim', False)
        self.isMinusMeanEmgData = kwargs['kwargs_pre'].get('isMinusMeanEmgData', False)
        self.segment = kwargs['kwargs_pre'].get("segment", 0)
        self.emgChannel = kwargs['kwargs_pre'].get("emgChannel", None)

    def DataCut(self, ):
        '''数据截切
            
        '''
        self.emg, self.imu = cut_data(self.emg, self.imu)
    
    def DataStretch(self, ):
        '''数据拉伸
            
        '''
        stretcher = Stretch(self.data_time)
        self.emg, self.imu = stretcher.stretch(self.emg, self.imu)
    

    def DataFill(self, emg_value = 0,  imu_value = 0):
        '''数据填充

           args:
                emg_value:emg数据的填充值
                imu_value:imu数据的填充值
        '''
        emg_line_len = self.data_time * 200
        imu_line_len = self.data_time * 50
        emg_count, imu_count = len(self.emg), len(self.imu)
        ## 处理emg数据
        self.emg = Data_Complement(self.emg, emg_line_len)
        # if emg_count < emg_line_len:
        #     emg_add = np.array([[emg_value for i in range(8)] for j in range(emg_line_len - emg_count)])
        #     self.emg = np.vstack([np.array(self.emg), emg_add])
        # else:
        #     self.emg = np.array(self.emg[0:emg_line_len])
        ## 处理imu数据
        self.imu = Data_Complement(self.imu, imu_line_len)
        # if imu_count < imu_line_len:
        #     imu_add = np.array([[imu_value for i in range(10)] for j in range(imu_line_len - imu_count)])
        #     self.imu = np.vstack([np.array(self.imu), imu_add])
        # else:
        #     self.imu = np.array(self.imu[0:imu_line_len])

    def DataSegment(self, ):
        '''数据分割
            
        '''
        if (len(self.emg) % self.segment != 0) or (len(self.imu) % self.segment != 0):
            print(len(self.emg) / self.segment)
            raise InterruptedError("the len / segment must be int!")
        else:
            self.emg = self.emg.reshape(self.segment, int(self.emg.shape[0] / self.segment), -1)
            self.imu = self.imu.reshape(self.segment, int(self.imu.shape[0] / self.segment), -1)
    
    # ## 数据归整
    # def DataNorm(self, ):
    #     self.emg = 

    def DataFilter(self, ):
        '''对EMG和IMU数据进行滤波操作

            args：
                Filter_args:
                    methold：滤波方式["butter", "wave"]
                    butter_srgs:
                        EmgCategory：EMG信号的滤波形式，lowpass[低通滤波]，highpass[高通滤波]，bandpass[带通滤波]，bandtop[带阻滤波]
                        EmgWn：选择EMG信号滤波的阈值
                        EmgOrder：EMG信号滤波阶数
                        ImuCategory：IMU信号的滤波形式，lowpass[低通滤波]，highpass[高通滤波]，bandpass[带通滤波]，bandtop[带阻滤波]
                        ImuWn：选择IMU信号滤波的阈值
                        ImuOrder：IMU信号滤波阶数
                    wave_args:
                        w：选择的小波函数
        '''
        if self.Filter_args['methold'] == "butter":
            butter_args = self.Filter_args["butter_args"]
            self.emg = butter_filter(self.emg, category = butter_args['EmgCategory'], Wn=butter_args['EmgWn'], order = butter_args['EmgOrder'])
            self.imu = butter_filter(self.imu, category = butter_args['ImuCategory'], Wn=butter_args['ImuWn'], order = butter_args['ImuOrder'])
        elif self.Filter_args['methold'] == "wave":
            wave_args = self.Filter_args["wave_args"]
            self.emg = Wave_filter(self.emg, wave_args['w'])
            self.imu = Wave_filter(self.imu, wave_args['w'])
        else:
            raise KeyError("Please change Filter methold!")

    def GetEmgFrequency(self, ):
        '''获得肌电流频域信息
           可以使用快速傅里叶变换或者小波变换
        '''
        ## 使用快速傅里叶变换进项时域到频域的转换--->得到的频域信号是一个复数形式的数据
        self.emg_F = fft(self.emg)

    def IncreaseEmgDim(self, ):
        '''增加肌电流维数
            
        '''
        Add_Data = self.emg.copy()
        for i in range(len(self.emg[0])-1):
            for j in range(i+1, len(self.emg[0])):
                Add_Data = np.hstack([Add_Data, np.abs(self.emg[:,i] - self.emg[:,j]).reshape(len(self.emg),1)])
        return Add_Data
    
    def SelectEmgChannel(self, ):
        """选择肌电流数据的通道
        
        """
        if self.emgChannel:
            self.emg = self.emg[:, self.emgChannel]
        else:
            pass

    def CorrectEmgData(self, ):
        '''肌电流维度矫正
            
        '''
        self.emg = correct(self.emg)

    def MinusMeanEmgData(self, ):
        '''肌电流数据去除设备噪音：每一维度减去均值

        '''
        self.emg = self.emg - np.mean(self.emg, axis=0)

    def DataPreprocess(self, emg, imu):
        '''数据处理

            args:
                isFilter：决定数据是否需要滤波
                isCut: 决定数据是否需要裁切
                isStretch: 决定数据是否需要拉伸
                data_time: 拉伸到data_time时间长度
                isFill: 决定数据是否需要填补
                isIncreEmgDim: 决定EMG数据是否需要扩充维度
                isMinusMeanEmgData：决定EMG数据每一维是否减去均值
                segment：数据裁剪个数

            return:
                EmgData, ImuData --> numpy
        '''
        self.emg, self.imu = emg, imu
        if ( self.emg.size ==0 ) or ( self.imu.size ==0):
            raise ValueError("数据不能为空")
        if self.isFilter:
            self.DataFilter()
        if self.isCut:
            self.DataCut()
        if self.isStretch:
            self.DataStretch()
        if self.isFill:
            self.DataFill()
        if self.isMinusMeanEmgData:
            self.MinusMeanEmgData()
        self.SelectEmgChannel()
        if self.isIncreEmgDim:
            self.emg = self.IncreaseEmgDim()
        if self.segment:
            self.DataSegment()
        
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
                    IMUFeatureType:提取IMU数据的特征类型，包括：[EULERANGLE, MEAN, SUM, VAR, STD]
        '''
        self.emg, self.imu = None, None
        # kwargs = kwargs['kwargs']
        # print(kwargs)
        self.kwargs_pre = kwargs['kwargs_pre']
        self.kwargs_feature = kwargs['kwargs_feature']  
        self.dataPre = DataPreprocessing(kwargs_pre = self.kwargs_pre)

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
            raise KeyError("The EMGFeatureKwargs don't have \"ZC_threshold\" !")
        if ('MYOP' in EMGFeatureTypes) and ('MYOP_threshold' not in EMGFeatureKwargs):
            raise KeyError("The EMGFeatureKwargs don't have \"MYOP_threshold\" !")
        if ('WAMP' in EMGFeatureTypes) and ('WAMP_threshold' not in EMGFeatureKwargs):
            raise KeyError("The EMGFeatureKwargs don't have \"WAMP_threshold\" !")
        if ('SSC' in EMGFeatureTypes) and ('SSC_threshold' not in EMGFeatureKwargs):
            raise KeyError("The EMGFeatureKwargs don't have \"SSC_threshold\" !")
        if ('MAVSLP' in EMGFeatureTypes) and ('MAVSLP_K' not in EMGFeatureKwargs):
            raise KeyError("The EMGFeatureKwargs don't have \"MAVSLP_K\" !")
        if ('V' in EMGFeatureTypes) and ('v' not in EMGFeatureKwargs):
            raise KeyError("The EMGFeatureKwargs don't have \"v\" !")
        if ('MAVSLP' in EMGFeatureTypes) and ('MAVSLP_K' not in EMGFeatureKwargs):
            raise KeyError("The EMGFeatureKwargs don't have \"MAVSLP_K\" !")
        if ('MHW' in EMGFeatureTypes) and ('MHW_K' not in EMGFeatureKwargs):
            raise KeyError("The EMGFeatureKwargs don't have \"MHW_K\" !")
        if ('MTW' in EMGFeatureTypes) and ('MTW_K' not in EMGFeatureKwargs):
            raise KeyError("The EMGFeatureKwargs don't have \"MTW_K\" !")
        if ('TM_N' in EMGFeatureTypes) and ('N' not in EMGFeatureKwargs):
            raise KeyError("The EMGFeatureKwargs don't have \"N\" !")
        feature_list = []
        for EMGFeatureType in EMGFeatureTypes:
            Fea = []
            if self.kwargs_pre["segment"]:
                for i in range(len(self.emg)):
                    feature = EMGDataFeature(self.emg[i])
                    Fea.append(feature.getFeature(EMGFeatureType, kwargs = EMGFeatureKwargs))
            else:
                feature = EMGDataFeature(self.emg)
                Fea.append(feature.getFeature(EMGFeatureType, kwargs = EMGFeatureKwargs)) 
            feature_list.append(Fea)
        return np.array(feature_list, dtype=object)

    ## 提取imu信号特征
    def ImuFeature(self, ):
        IMUFeatureTypes = self.kwargs_feature['IMUFeatureTypes']
        imu_Euler_angle = []
        feature_list = []
        for IMUFeatureType in IMUFeatureTypes:
            Fea = []
            if self.kwargs_pre["segment"]:
                for i in range(len(self.imu)):
                    feature = IMUDataFeature(self.imu[i])
                    Fea.append(feature.getFeature(IMUFeatureType))


                    # pitch, roll, yaw = data_change(self.imu[s])
                    # angle = []
                    # # for i in range(len(pitch)):
                    # #     feature = [0 for i in range(7)]
                    # #     feature[0] = self.imu[s][i][0]
                    # #     feature[1] = self.imu[s][i][1]
                    # #     feature[2] = self.imu[s][i][2]
                    # #     feature[3] = self.imu[s][i][3]
                    # #     feature[4] = pitch[i]
                    # #     feature[5] = roll[i]
                    # #     feature[6] = yaw[i]
                    # angle.append(np.concatenate((self.imu[s][:,:4], pitch.reshape(self.imu[s].shape[0],1), roll.reshape(self.imu[s].shape[0],1), yaw.reshape(self.imu[s].shape[0],1)), axis=1))
                    # imu_Euler_angle.append(angle)
                # return np.array(imu_Euler_angle)
            else:
                feature = IMUDataFeature(self.imu)
                Fea.append(feature.getFeature(IMUFeatureType))
                # pitch, roll, yaw = data_change(self.imu)
                # return np.concatenate((self.imu[:,:4], pitch.reshape(self.imu.shape[0],1), roll.reshape(self.imu.shape[0],1), yaw.reshape(self.imu.shape[0],1)), axis=1)
            feature_list.append(Fea)
        return np.array(feature_list, dtype=object)

    def getFeature(self, emg, imu):
        '''整合信号

        '''
        self.emg, self.imu = emg, imu
        if (self.emg.size == 0) or (self.imu.size == 0):
            raise ValueError("数据不能为空")
        ## 数据预处理
        self.emg, self.imu = self.dataPre.DataPreprocess(self.emg, self.imu)
        ## 特征提取
        emgFeature = self.EmgFeature()
        imuFeature = self.ImuFeature()
        emgFeature = np.array(emgFeature, dtype=object).T
        imuFeature = np.array(imuFeature, dtype=object).T

        return emgFeature, imuFeature
        
## 数据提取的生成器
def ReadData(dataPath):
    ## 读取emg数据文件名
    emgDataNames = os.listdir(dataPath + 'emg/')
    for emgDataName in emgDataNames:
        emgDataPath = dataPath + 'emg/' + emgDataName
        imuDataPath = emgDataPath.replace('emg', 'imu')
        ## 获取emg和imu数据
        emg = ReadFile(emgDataPath, DataType= "int")
        imu = ReadFile(imuDataPath, DataType= "float")
        ## 生成label
        fuhao = ',\!?。，？！、 '
        for x in fuhao:
            if x in emgDataName:
                emgDataName = emgDataName.replace(x,'')
        label = emgDataName.split('_')[0].split('-')
        ## 生成志愿者
        scale = emgDataName.split('_')[-3]
        yield emg, imu, label, scale

## 数据处理生成器
def dataGenerator(dataPath, LabelGenerator, **kwargs):
    data = ReadData(dataPath)
    dataPreproce = DataPreprocessing(kwargs_pre=kwargs ["kwargs_pre"])
    while True:
        try:
            emg, imu, label, scale = next(data)
            emgPre, imuPre = dataPreproce.DataPreprocess(emg, imu)
            label = LabelGenerator(label)
            yield np.array(emgPre), np.array(imuPre), np.array(label), scale
        except StopIteration:
            return

## 数据特征生成器
def dataFeature(dataPath, LabelGenerator, **kwargs):
    data = ReadData(dataPath)
    dataFeatureExtract = ExtractDataFeature(kwargs_pre= kwargs["kwargs_pre"], kwargs_feature=kwargs["kwargs_feature"])
    while True:
        try:
            emg, imu, label, scale = next(data)
            emg_feature, imu_feature = dataFeatureExtract.getFeature(emg, imu)
            label = LabelGenerator(label)
            yield np.array(emg_feature), np.array(imu_feature), np.array(label), scale
        except StopIteration:
            return

## 读取双手手势数据
def ReadTHData(LeftDataPath, RightDataPath):
    ## 读取emg数据文件名
    LeftEMGDataNames = os.listdir(LeftDataPath + 'emg/')
    RightEMGDataNames = os.listdir(RightDataPath + 'emg/')
    try:
        for LeftEMGDataName, RightEMGDataName in zip(LeftEMGDataNames, RightEMGDataNames):
            LeftEMGDataPath = LeftDataPath + 'emg/' + LeftEMGDataName
            LeftIMUDataPath = LeftEMGDataPath.replace('emg', 'imu')
            RightEMGDataPath = RightDataPath + 'emg/' + RightEMGDataName
            RightIMUDataPath = RightEMGDataPath.replace('emg', 'imu')
            ## 获取emg和imu数据
            Leftemg = ReadFile(LeftEMGDataPath, DataType= "int")
            Leftimu = ReadFile(LeftIMUDataPath, DataType= "float")
            Rightemg = ReadFile(RightEMGDataPath, DataType= "int")
            Righrimu = ReadFile(RightIMUDataPath, DataType= "float")
            ## 生成label
            fuhao = ',\!?。，？！、 '
            for x in fuhao:
                if x in LeftEMGDataName and x in RightEMGDataName:
                    LeftEMGDataName = LeftEMGDataName.replace(x,'')
                    RightEMGDataName = RightEMGDataName.replace(x,'')
            Leftlabel = LeftEMGDataName.split('_')[0].split('-')
            Rightlabel = RightEMGDataName.split('_')[0].split('-')
            if operator.eq(Leftlabel,Rightlabel) == False:
                raise ValueError("left-right hand mismatch.")
            ## 生成志愿者
            scale = LeftEMGDataName.split('_')[-3]
            yield Leftemg, Leftimu, Rightemg, Righrimu, Leftlabel, scale
    except ValueError as e:
        print("ValueError:",e)
        pass

## 双手数据处理生成器
def dataTHGenerator(dataPath, LabelGenerator, **kwargs):
    data = ReadTHData(dataPath["Left"], dataPath["Right"])
    dataPreproce = DataPreprocessing(kwargs_pre=kwargs ["kwargs_pre"])
    while True:
        try:
            Leftemg, Leftimu, Rightemg, Rightimu, label, scale = next(data)
            LeftemgPre, LeftimuPre = dataPreproce.DataPreprocess(Leftemg, Leftimu)
            RightemgPre, RightimuPre = dataPreproce.DataPreprocess(Rightemg, Rightimu)
            label = LabelGenerator(label)
            yield np.array(LeftemgPre), np.array(LeftimuPre), np.array(RightemgPre), np.array(RightimuPre), label, scale
        except StopIteration:
            return

## 双手数据特征生成器
def dataTHFeature(dataPath, LabelGenerator, **kwargs):
    data = ReadTHData(dataPath["Left"], dataPath["Right"])
    dataFeatureExtract = ExtractDataFeature(kwargs_pre= kwargs["kwargs_pre"], kwargs_feature=kwargs["kwargs_feature"])
    while True:
        try:
            Leftemg, Leftimu, Rightemg, Rightimu, label, scale = next(data)
            Leftemg_feature, Leftimu_feature = dataFeatureExtract.getFeature(Leftemg, Leftimu)
            Rightemg_feature, Rightimu_feature = dataFeatureExtract.getFeature(Rightemg, Rightimu)
            label = LabelGenerator(label)
            yield np.array(Leftemg_feature), np.array(Leftimu_feature), np.array(Rightemg_feature), np.array(Rightimu_feature), label, scale
        except StopIteration:
            return