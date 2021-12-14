# DataPreProcess_packages
The data collected by MYO bracelet is preprocessed, including data cutting, stretching, filling and feature extraction.
## How to use this package
### 1、Install related packages
```shell
pip install Requirement.txt
```
### 2、Use&Install the data preprocessing package
- Not to install
```
git clone https://github.com/ZhangJiangtao-0108/DataPreProcess_packages.git
```
```python
import sys
sys.path.append("packages path")
```
- install
```
pip install DataPreProcess_packages-1.0.tar.gz
```
### 3、Import package
```python
from DataPreProce import *
```

## Features of EMG data
- IEMG: Definiyion of IEMG feature is definend as a summation of absolute value of the EMG sign amplitude.
- MAV: Mean absolute value(MAV) feature is an aberage of absolute value of the EMG signal amplituden in a segment.
- MAV1：Modified mean absolute value type 1 (MAV1) is an extension of MAV feature. The weighted window function wi is assigned into the equation for improving robustness of MAV feature.
- MAV2: Modified mean absolute value type 2 (MAV2) is an expansion of MAV feature which is similar to the MAV1 Phinyomark et al., 2009a). However, the weighted window function wi that s assigned into the equation is a continuous function. It improves smoothness of the weighted function.
- SSI: Simple square integral (SSI) or integral square uses energy of the EMG signal as a feature. It is a summation of square values of the EMG signal amplitude. Generally, this parameter is defined as an energy index.
- VAR: variance is defined as an average of square values of the deviation of that variable.
- TM_N: Temporal moment is a statistical analysis. the absolute value was taken to greatly reduce the within class separation for the odd moment case.
- RMS: Root mean square (RMS) is another popular feature in analysis of the EMG signal. It is also similar to standard deviation method.
- V: The v-Order (V) is a non-linear detector that implicitly estimates muscle contraction force.
- LOG: Like the V feature, this feature also provides an estimate of the muscle contraction force.
- WL: Like the V feature, this feature also provides an estimate of the muscle contraction force. It is defined as cumulative length of the EMG waveform over the time segment. Some literatures called this feature as wavelength (WAVE).
- ACC: Average amplitude change (AAC) is nearly equivalent to WL feature, except that wavelength is averaged. A number of research studies called this feature as difference absolute mean value (DAMV); however, its definition divides WL value by length N minus one.
- DASDV: Difference absolute standard deviation value (DASDV) is look like RMS feature, in other words, it is a standard deviation value of the wavelength.
- ZC: Zero crossing (ZC) is a measure of frequency information of the EMG signal that is defined in time domain. It is a number of times that amplitude values of the EMG signal cross zero amplitude level. To avoid lowvoltage fluctuations or background noises, threshold condition is implemented.
- MYOP: Myopulse percentage rate (MYOP) is an average value of myopulse output which is defined as one when absolute value of the EMG signal exceeds a pre-defined threshold value.
- WAMP: Willison amplitude or Wilson amplitude (WAMP) is a measure of frequency information of the EMG signal as same as defines in ZC feature. It is a number of times resulting from difference between the EMG signal amplitude among two adjoining segments that exceeds a pre-defined threshold.
- SSC: Slope sign change (SSC) is related to ZC, MYOP, and WAMP features. It is another method to represent frequency information of the EMG signal. It is a number of times that slope of the EMG signal changes sign. The number of changes between the positive and negative slopes among three sequential segments is performed with the threshold function for avoiding background noise in the EMG signal.
- MAVSLP: Mean absolute value slope (MAVSLP) is a modified version of MAV feature to establish multiple features. Differences between MAVs of the adjacent segments are determined.
- MHW: Multiple hamming windows (MHW) are an original version of multiple time windows method. The raw EMG signal is segmented by the Hamming windows on all time series. The MHW features are computed using each window’s energy.
- MTW: Multiple trapezoidal windows (MTW) are one type of the multiple time windows method.  Like the MHW, this feature method uses the energy contained inside a window as feature values, but the function of window w is changing from the Hamming windows to the trapezoidal windows, which in Du’s study, the trapezoidal windowing function performed the best ones. 
- HIST: 
- AR: 
- CC: 
## Features of IMU data
- Quaternion to Euler Angle
## Parameter Settings
### 1.Data processing and feature extraction parameter setting
```json
kwargs = {
    "kwargs_pre":{
                  "isCut":True,
                  "isStretch":True,
                  "data_time":4, 
                  "isFill":False,
                  "isFilter":False,
                  "Filter_args":{
                                "EmgCategory":'lowpass',
                                "EmgWn":0.8,
                                "EmgOrder":8,
                                "ImuCategory":'lowpass',
                                "ImuWn":0.8,
                                "ImuOrder":8
                  },
                  "isMinusMeanEmgData":True,
                  "isIncreEmgDim":False,
                  "segment":100
                   },
    "kwargs_feature":{
                    "EMGFeatureType":["IEMG"," MAV", "MAV1", "MAV2", "SSI", "VAR", "TM_N", "RMS", "V", "LOG", "WL", "AAC", "DASDV", "ZC", "MYOP", "WAMP", "SSC", "MAVSLP", "MHW", "MTW", "HIST", "HIST", "AR", "CC"],
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
```
#### 'kwargs_pre' Parameter interpretation
| Parameter | Describe |
|-----------|----------|
| isCut | Determine if the data needs to be cutted |
| isStretch | Determine if the data needs to be stretched |
| data_time | Determine the data stretch length |
| isFill | Determine if the data needs to be filling |
| isFilter | Determine if the data needs to be filted |
| Filter_args | Determine if the data needs to be stretched |
| isMinusMeanEmgData | Determine if the EMG data needs to be subtracted from the mean |
| isIncreEmgDim | Determine whether the EMG data needs to be dimensioned |
| segment | Number of data segments |
#### EMG data feature table
| EMGFeatureTypes | parameter | describe |
|-----------------|-----------|----------|
| IEMG | None | None |
| MAV | None | None |
| MAV1 | None | None |
| MAV2 | None | None |
| SSI | None | None |
| VAR | None | None |
| TM_N | N | Order Number, The default value of 2 |
| RMS | None | None |
| V | v | is the vorresponding of the feature V, the default value is 1 |
| LOG | None | None |
| WL | None | None |
| AAC | None | None |
| DASDV | None | None |
| ZC | ZC_threshold | is numerical boundary, The default value of 0 |
| MYOP | MYOP_threshold | is numerical boundary, The default value of 0 |
| WAMP | WAMP_threshold | is numerical boundary, The default value of 0 |
| SSC | SSC_thresholdNone | is numerical boundary, The default value of 0 |
| MAVSLP | MAVSLP_K | is number of segments covering the EMG signal, The default value of 3 |
| MHW | MHW_K | is the size of the hamming windows, the default value is 1 |
| MTW | MTW_K | is the size of the hamming windows, the default value is 1 |
### 2.DataSets parameter setting
```json
kwargs = {  "DataPath":"C:/Users/张江涛/Desktop/imu测试/imu_sentence数据/",
            "SaveDataPath":"C:/Users/张江涛/Desktop/imu测试/imu_sentence数据/",
            "gesture_dic_path":"C:/Users/张江涛/Desktop/新建文件夹/gesture_sentence_recognition/config/gesture_dic_all.txt",
            "label_scales_path":"C:/Users/张江涛/Desktop/新建文件夹/gesture_sentence_recognition/config/label_scales.txt",
            "sentence_max_label":9,
            "DataPre_args":{
                        "kwargs_pre":{
                                    "isCut":True,
                                    "isStretch":True,
                                    "data_time":4, 
                                    "isFill":True,
                                    "isMinusMeanEmgData":False,
                                    "isIncreEmgDim":True,
                                    "segment":100
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
```
## References
[1]. Feature reduction and selection for EMG signal classification

