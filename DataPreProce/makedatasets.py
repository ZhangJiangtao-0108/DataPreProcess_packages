'''
    制作数据集
'''
from tqdm import tqdm
import h5py
import numpy as np
import os
from DataPre import dataGenerator

def MakeDataSets(kwargs):
    """制作数据集

        args:
            DataSets_kwargs:数据集参数
                DataPath:数据路径
                SaveDataPath:保存数据集路径
                gesture_dic_path:手势字典的路径
                label_scales_path:志愿者编号文件路径
                sentence_max_label:label的长度
            DataPre_kwargs:
                kwargs_pre:
                    isFilter：决定数据是否需要滤波
                    isCut: 决定数据是否需要裁切
                    isStretch: 决定数据是否需要拉伸
                    data_time: 拉伸到data_time时间长度
                    isFill: 决定数据是否需要填补
                    isIncreEmgDim: 决定EMG数据是否需要扩充维度
                    isMinusMeanEmgData：决定EMG数据每一维是否减去均值
                    segment：数据裁剪个数
                kwargs_feature:
                    EMGFeatureType: 提取EMG数据的特征类型，包括：[IEMG, MAV, MAV1, MAV2, SSI, VAR, TM_N, RMS, V, LOG, WL, AAC, DASDV, ZC, MYOP, WAMP, SSC, MAVSLP, MHW, MTW, HIST, HIST, AR, CC]
                    EMGFeatureKwargs: 对应EMG数据特征的参数
                        ZC_threshold: ZC对应的阈值，默认值为0
                        MYOP_threshold: MYOP对应的阈值，默认值为0
                        WAMP_threshold: WAMP对应的阈值，默认值为0
                        SSC_threshold: SSC对应的阈值，默认值为0
                        K: MAVSLP的特征参数，EMG数据对应的分段数，默认值为3
                        N: TM_N对应的阶数

    """
    ## 设置数据集参数
    DataSets_kwargs = kwargs["DataSets_kwargs"]
    ## 设置数据处理参数
    DataPre_kwargs = kwargs["DataPre_kwargs"]
    # print(DataPre_kwargs)
    DataPath = DataSets_kwargs['DataPath']
    ## 读取字典
    gesture_dic_file = open(DataSets_kwargs['gesture_dic_path'],'r',encoding='gbk')
    gesture_dic = eval(gesture_dic_file.readline())
    gesture_dic_file.close()
    ## 读取志愿者编号
    label_scales_file = open(DataSets_kwargs['label_scales_path'],'r',encoding='gbk')
    label_scales = eval(label_scales_file.readline())
    label_scales_file.close()
    ## 获取数据个数
    filenames = os.listdir(DataPath + 'emg/')
    DataNum = len(filenames)
    # print(DataPre_kwargs)
    emg, imu, _, _ = next(dataGenerator(DataPath, kwargs = DataPre_kwargs))
    ## 创建dataSets文件
    dataSetsPath = DataSets_kwargs['SaveDataPath'] + 'datasets_feature_All.hdf5'  
    datasets = h5py.File(dataSetsPath,'w')
    ## emg数据特征类型
    emgFeatureTypes = DataPre_kwargs["kwargs_feature"]["EMGFeatureTypes"]
    for i in range(len(emg)):
        featureShape = tuple((DataNum,)) + tuple(emg[i].shape) #+ tuple((8,))
        # print(featureShape)
        datasets.create_dataset('emg_data_' + emgFeatureTypes[i], featureShape)
    imu_feature_value = datasets.create_dataset('imu_data',(DataNum,imu.shape[0],imu.shape[1],imu.shape[2]))
    label_value = datasets.create_dataset('labels',(DataNum,DataSets_kwargs['sentence_max_label']))
    scale_value = datasets.create_dataset('scales',(DataNum,1))
    ## 数据迭代器
        ## 创建dataSets文件
    emg, imu, _, _ = next(dataGenerator(DataPath, kwargs = DataPre_kwargs))
    data = iter(dataGenerator(DataPath, kwargs = DataPre_kwargs))
    try:
        for (emg, imu, sentence_word, scale), i in zip(data, tqdm(range(DataNum))):
            for j in range(len(emg)):
                # print(type(emg[j]))
                # print(datasets["emg_data_"+emgFeatureTypes[j]][i].shape)
                emg_feature_value = datasets["emg_data_"+emgFeatureTypes[j]]
                # datasets["emg_data_"+emgFeatureTypes[j]][i] = emg[j] 
                # print(list(emg[j]))
                emg_feature_value[i] = list(emg[j])
            imu_feature_value[i] = imu
            ## 生成label
            label = [gesture_dic[word] for word in sentence_word]
            if len(label) < DataSets_kwargs['sentence_max_label']:
                label.insert(0,gesture_dic['sos'])
                # label.insert(len(label), gesture_dic['eos'])
                if len(label) < DataSets_kwargs['sentence_max_label']:
                    for k in range(len(label),DataSets_kwargs['sentence_max_label']):
                        label.insert(k,gesture_dic['pos'])
            print(filenames[i])
            print(label)
            label_value[i] = label
            scale_value[i] = label_scales[scale]
    except StopIteration:
        pass
    datasets.close()

def ReadDataSets(**kwargs):
    """
        读取特征数据

        args:
            dataSetsPath:数据集的路径
            EMGFeatureTypes:选择的emg数据的特征
            IMUFeatureTypes:


    """
    datasets = h5py.File(kwargs["dataSetsPath"],'r')
    datasets.close()

if __name__ == '__main__':
    kwargs = {
        "DataSets_kwargs": {
                            "DataPath":"/home/w/数据/zjt/sentence_data/sentence_data_train/",
                            "SaveDataPath":"/home/zjt/zhangjiangtao/sentence_data/",
                            'gesture_dic_path':'/home/zjt/zhangjiangtao/sentence_data/gesture_dic_all.txt',
                            'label_scales_path':'/home/zjt/zhangjiangtao/sentence_data/label_scales.txt',
                            'sentence_max_label':9
                            },
        "DataPre_kwargs" : {  
                            "kwargs_pre":{
                                    "isCut":True,
                                    "isStretch":True,
                                    "data_time":4, 
                                    "isFill":False,
                                    "isFilter":True,
                                    "Filter_args":{
                                                    "methold":"wave",
                                                    "butter_args":{
                                                                    "EmgCategory":'lowpass',
                                                                    "EmgWn":0.8,
                                                                    "EmgOrder":8,
                                                                    "ImuCategory":'lowpass',
                                                                    "ImuWn":0.8,
                                                                    "ImuOrder":8
                                                    },
                                                    "wave_args":{
                                                                "w":"db7"
                                                    }
                                    },
                                    "isMinusMeanEmgData":True,
                                    "isIncreEmgDim":False,
                                    "segment":100
                                    },
                                "kwargs_feature":{
                                        "EMGFeatureTypes":["IEMG","MAV", "MAV1", "MAV2", "SSI", "VAR", "TM_N", "RMS", "V", "LOG", "WL", "AAC", "DASDV", "ZC", "MYOP", "WAMP", "SSC", "MHW", "MTW",], 
                                        "EMGFeatureKwargs":{
                                                            "ZC_threshold":0,
                                                            "MYOP_threshold":0,
                                                            "WAMP_threshold":0,
                                                            "SSC_threshold":0,
                                                            "v":1,
                                                            "MAVSLP_K":3,
                                                            "MHW_K":1,
                                                            "MTW_K":1,
                                                            "N":2
                                                            }
                            },
                                }
            }
    # MakeDataSets(kwargs)
    ReadDataSets(kwargs)
