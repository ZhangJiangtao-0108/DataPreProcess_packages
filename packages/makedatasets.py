'''
    制作数据集
'''
from tqdm import tqdm
import h5py
import os
from DataPre import dataGenerator

def MakeDataSets(dataPath, **kwargs):
    '''制作数据集

        args:
            datasets_args:数据集参数
                gesture_dic_path:手势字典的路径
                label_scales_path:志愿者编号文件路径
                sentence_max_label:label的长度
    '''
    ## 设置数据集参数
    print(kwargs)
    datasets_args = kwargs['datasets_args']
    ## 设置数据处理参数
    dataPre_args = kwargs.pop('dataPre_args', False)
    ## 读取字典
    gesture_dic_file = open(datasets_args['gesture_dic_path'],'r')
    gesture_dic = eval(gesture_dic_file.readline())
    gesture_dic_file.close()
    ## 读取志愿者编号
    label_scales_file = open(datasets_args['label_scales_path'],'r')
    label_scales = eval(label_scales_file.readline())
    label_scales_file.close()
    ## 获取数据个数
    DataNum = len(os.listdir(dataPath + 'emg/'))
    emg, imu, _, _ = next(dataGenerator(dataPath))
    ## 创建dataSets文件
    dataSetsPath = dataPath + 'datasets_feature_All.hdf5'
    datasets = h5py.File(dataSetsPath,'w')
    emg_feature_value = datasets.create_dataset('emg_data',(DataNum,emg.shape[0],emg.shape[1]))
    imu_feature_value = datasets.create_dataset('imu_data',(DataNum,imu.shape[0],imu.shape[1]))
    label_value = datasets.create_dataset('labels',(DataNum,datasets_args['sentence_max_label']))
    scale_value = datasets.create_dataset('scales',(DataNum,1))
    ## 数据迭代器
    data = iter(dataGenerator(dataPath))
    try:
        for (emg, imu, sentence_word, scale), i in zip(data, tqdm(range(DataNum))):
            emg_feature_value[i] = emg
            imu_feature_value[i] = imu
            ## 生成label
            label = [gesture_dic[word] for word in sentence_word]
            if len(label) < datasets_args['sentence_max_label']:
                label.insert(0,gesture_dic['sos'])
                # label.insert(len(label), gesture_dic['eos'])
                if len(label) < datasets_args['sentence_max_label']:
                    for i in range(len(label),datasets_args['sentence_max_label']):
                        label.insert(i,gesture_dic['pos'])
            
            label_value[i] = label
            scale_value[i] = label_scales[scale]
    except StopIteration:
        pass
    datasets.close()


if __name__ == '__main__':

    dataPath = r'C:/Users/张江涛/Desktop/imu测试/imu_sentence数据/'
    kwargs = {'datasets_args':{'gesture_dic_path':'C:/Users/张江涛/Desktop/新建文件夹/gesture_sentence_recognition/config/gesture_dic_all.txt',
                               'label_scales_path':'C:/Users/张江涛/Desktop/新建文件夹/gesture_sentence_recognition/config/label_scales.txt',
                               'sentence_max_label':9
                              }

    }
    datasets_args = {'gesture_dic_path':'C:/Users/张江涛/Desktop/新建文件夹/gesture_sentence_recognition/config/gesture_dic_all.txt',
                     'label_scales_path':'C:/Users/张江涛/Desktop/新建文件夹/gesture_sentence_recognition/config/label_scales.txt',
                     'sentence_max_label':9
    }
    MakeDataSets(dataPath, datasets_args = datasets_args)
