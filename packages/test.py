from DataPre import dataGenerator


if __name__ == '__main__':
    datapath =  r'C:/Users/张江涛/Desktop/imu测试/imu_sentence数据/'
    kwargs = {
    "kwargs_pre":{
                  "isCut":True,
                  "isStretch":True,
                  "data_time":4, 
                  "isFill":True,
                  "isIncreEmgDim":True
                   },
    "kwargs_feature":{
                    "EMGFeatureTypes":["MTW"], 
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
dataFeature = iter(dataGenerator(datapath, kwargs))
for emg_feature, imu_feature, label, scale in dataFeature:
    # print(emg_feature.shape)
    # print(imu_feature.shape)
    print(label)
    print(scale)