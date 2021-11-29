'''
    制作数据集
'''
from tqdm import tqdm
import h5py
import os
from DataPre import dataGenerator

def MakeDataSets(kwargs):
    '''制作数据集

        args:
            datasets_args:数据集参数
                gesture_dic_path:手势字典的路径
                label_scales_path:志愿者编号文件路径
                sentence_max_label:label的长度
    '''
    ## 设置数据集参数
    # print(kwargs)
    # datasets_args = kwargs['datasets_args']
    DataPath = kwargs['DataPath']
    ## 设置数据处理参数
    dataPre_args = kwargs['DataPre_args']
    ## 读取字典
    gesture_dic_file = open(kwargs['gesture_dic_path'],'r')
    gesture_dic = eval(gesture_dic_file.readline())
    gesture_dic_file.close()
    ## 读取志愿者编号
    label_scales_file = open(kwargs['label_scales_path'],'r')
    label_scales = eval(label_scales_file.readline())
    label_scales_file.close()
    ## 获取数据个数
    DataNum = len(os.listdir(DataPath + 'emg/'))
    emg, imu, _, _ = next(dataGenerator(DataPath, dataPre_args))
    ## 创建dataSets文件
    if kwargs['SaveDataPath']:
        dataSetsPath = kwargs['SaveDataPath'] + 'datasets_feature_All.hdf5'
    else:
        dataSetsPath = kwargs['DataPath'] + 'datasets_feature_All.hdf5'
    datasets = h5py.File(dataSetsPath,'w')
    emg_feature_value = datasets.create_dataset('emg_data',(DataNum,emg.shape[0],emg.shape[1]))
    imu_feature_value = datasets.create_dataset('imu_data',(DataNum,imu.shape[0],imu.shape[1]))
    label_value = datasets.create_dataset('labels',(DataNum,kwargs['sentence_max_label']))
    scale_value = datasets.create_dataset('scales',(DataNum,1))
    ## 数据迭代器
        ## 创建dataSets文件
    emg, imu, _, _ = next(dataGenerator(DataPath, dataPre_args))
    data = iter(dataGenerator(DataPath, dataPre_args))
    try:
        for (emg, imu, sentence_word, scale), i in zip(data, tqdm(range(DataNum))):
            emg_feature_value[i] = emg
            imu_feature_value[i] = imu
            ## 生成label
            label = [gesture_dic[word] for word in sentence_word]
            if len(label) < kwargs['sentence_max_label']:
                label.insert(0,gesture_dic['sos'])
                # label.insert(len(label), gesture_dic['eos'])
                if len(label) < kwargs['sentence_max_label']:
                    for i in range(len(label),kwargs['sentence_max_label']):
                        label.insert(i,gesture_dic['pos'])
            
            label_value[i] = label
            scale_value[i] = label_scales[scale]
    except StopIteration:
        pass
    datasets.close()


if __name__ == '__main__':

    kwargs = {'datasets_args':{'gesture_dic_path':'C:/Users/张江涛/Desktop/新建文件夹/gesture_sentence_recognition/config/gesture_dic_all.txt',
                               'label_scales_path':'C:/Users/张江涛/Desktop/新建文件夹/gesture_sentence_recognition/config/label_scales.txt',
                               'sentence_max_label':9
                              }

    }
    kwargs = {'DataPath':'C:/Users/张江涛/Desktop/imu测试/imu_sentence数据/',
                     'SaveDataPath':'C:/Users/张江涛/Desktop/imu测试/imu_sentence数据/',
                     'gesture_dic_path':'C:/Users/张江涛/Desktop/新建文件夹/gesture_sentence_recognition/config/gesture_dic_all.txt',
                     'label_scales_path':'C:/Users/张江涛/Desktop/新建文件夹/gesture_sentence_recognition/config/label_scales.txt',
                     'sentence_max_label':9,
                     'DataPre_args':{
                                    "kwargs_pre":{
                                                "isCut":True,
                                                "isStretch":True,
                                                "data_time":4, 
                                                "isFill":True,
                                                "isIncreEmgDim":True
                                                },
                                    "kwargs_feature":{
                                                    "EMGFeatureTypes":["SSI"], 
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
    MakeDataSets(kwargs)
