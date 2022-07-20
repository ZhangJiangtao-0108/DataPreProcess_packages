from numpy.core.numeric import count_nonzero
from numpy.core.records import array
from DataPre import  ReadData, ExtractDataFeature
import numpy as np
import matplotlib.pyplot as plt
from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis
from tqdm import tqdm
import os

if __name__ == '__main__':
    datapath =  r'D:/张江涛/实验/数据/word/'
    kwargs_pre={
                "isCut":True,
                "isStretch":True,
                "data_time":4, 
                "isFill":False,
                "isFilter":False,
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
                }
    kwargs_feature={
                    "EMGFeatureTypes":["IEMG","MAV","SSI","VAR","WL"], 
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
                                        },
                    "IMUFeatureTypes":["EULERANGLE", "MEAN", "SUM", "VAR", "STD"],
                    }
## emg 数据进行规整
def emgnorm(emg):
    emg = np.array(emg)
    for i in range(8):
        max_, min_ = max(emg[:,i]), min(emg[:,i])
        rate = 200 / (max_ - min_)
        emg[:,i] = emg[:,i] * rate
        # print(max_)
    return emg

def dataGenerator(dataPath, kwargs):
    data = ReadData(dataPath)
    dataFeatureExtract = ExtractDataFeature(kwargs = kwargs)
    while True:
        try:
            emg, imu, label, scale = next(data)
            # emg = emgnorm(emg)
            # emg = list(emg)
            emg_feature, imu_feature = dataFeatureExtract.getFeature(emg, imu)
            yield np.array(emg_feature), np.array(imu_feature), label, scale
        except StopIteration:
            return

def ReadEmg(emg_path):
    # f1 = open(emg_path, 'r')
    with open(emg_path, 'r') as f1:     
        emg = f1.read().strip().split('\n')
        for i in range(len(emg)):
            emg[i] = emg[i].strip().split(' ')
            emg[i] = [int(i) for i in emg[i]]         # 将字符串列表转换为int型列表
    
    imu_path = emg_path.replace('emg', 'imu')
    # f2 = open(imu_path, 'r')
    with open(imu_path, 'r') as f2:
        imu = f2.read().strip().split('\n')
        for i in range(len(imu)):
            imu[i] = imu[i].strip().split(' ')
            imu[i] = [float(i) for i in imu[i]]         # 将字符串列表转换为int型列表
    return emg, imu
# Data = iter(ReadData(datapath))
# dataFeature = dataGenerator(datapath, kwargs)
# emg_feature1, _, _, _ = next(dataFeature)
# emg_feature2, _, _, _ = next(dataFeature)
# print(data1)
## 数据特征提取器
dataFeatureExtrech = ExtractDataFeature(kwargs_pre = kwargs_pre, kwargs_feature= kwargs_feature)
names = os.listdir(datapath)
for name in names:
    filenames = os.listdir(datapath + name + '/emg/')
    ## 文件保存路径
    save_path = r'D:/张江涛/实验/EMG_dtw/word/cut_stretch_MinusMean/' + name + '/'
    for i, _ in zip(range(len(filenames)-1), tqdm(range(len(filenames) - 1))):
        for j in range(i+1, len(filenames)):
            ## 读取数据
            emg_path1 = datapath + name + '/emg/' + filenames[i]
            emg1, imu1 = ReadEmg(emg_path1)
            emg_path2 = datapath + name + '/emg/' + filenames[j]
            emg2, imu2 = ReadEmg(emg_path2)

            ## 处理数据
            emg_feature1, imu_feature1 = dataFeatureExtrech.getFeature(emg1, imu1)
            emg_feature2, imu_feature2 = dataFeatureExtrech.getFeature(emg2, imu2)
            emg_feature1 = np.array(emg_feature1)
            emg_feature2 = np.array(emg_feature2)
            # print(emg_feature1.shape)
            # print(emg_feature2.shape)
            ## 名称
            title = save_path + filenames[i].split('_')[1] + filenames[i].split('_')[2] + "vs" + filenames[j].split('_')[1] + filenames[j].split('_')[2] + '/'
            for k in range(len(emg_feature1)):
                # print(k)
                ## 创建文件夹
                title_ = title + kwargs_feature["EMGFeatureTypes"][k] + '/'
                if not os.path.exists(title_):
                    os.makedirs(title_)
                for dim in range(emg_feature1.shape[-1]):
                    distance, path = dtw.warping_paths(emg_feature1[k,:,dim], emg_feature2[k,:,dim])
                    path = dtw.warping_path(emg_feature1[k,:,dim], emg_feature2[k,:,dim])
                    dtwvis.plot_warping(emg_feature1[k,:,dim], emg_feature2[k,:,dim], path, filename=title_+ str(dim) + '-' + str(distance) + ".png")














# count = 0
# for (emg, imu, label, scale), (emg_feature, imu_feature, label, scale) in zip(Data, dataFeature):
#     # print(np.array(emg).shape)
#     # print(np.array(imu).shape)
#     # print(emg_feature.shape)
#     # print(imu_feature.shape)
#     # print(label)
#     # print(scale)
#     # print(max(np.array(emg)[:,1]))
#     emg = emgnorm(np.array(emg))
#     # print(max(emg[:,1]))
    
#     titile = str(label) + str(scale) + str(count)
#     a = plt.figure(figsize=(12, 8))
#     plt.title(titile) 
#     # # # b = plt.figure()
#     # for i in range(len(emg[0])):
#     #     # print(len(emg))
#     #     plt.subplot(4,4,i+1)
#     #     # print(len(np.array(emg)[:,i]))
#     #     plt.plot(range(0, len(emg), 1), np.array(emg)[:,i])
#     #     plt.subplot(4,4,i+1+8)
#     #     plt.plot(range(0,len(emg_feature[0]), 1), emg_feature[0,:,i])
#     # plt.savefig('C:/Users/张江涛/Desktop/emgImage1/' + titile + '.png')
#     # plt.show()

#     plt.plot(range(0, 8, 1), np.sum(np.array(emg), axis= 0)/len(emg))
#     plt.savefig('C:/Users/张江涛/Desktop/emgImage/' + titile + '.png')

#     count += 1