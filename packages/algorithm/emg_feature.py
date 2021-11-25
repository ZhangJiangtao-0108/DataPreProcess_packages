'''
    提取EMG信号的特征
'''
import numpy as np

class EMGDataFeature():
    def __init__(self, Data) -> None:
        self.Data = Data
        self.__DataLen = 0

    # @classmethod

    @property.setter
    def Data(self, Data):
        self.Data = Data
        self.__DataLen = len(self.Data)

    def IEMG(self, ):
        '''
            Definiyion of IEMG feature is definend as a summation of absolute value of the EMG sign amplitude.
        '''
        IEMGFeature = np.sum(np.abs(self.Data), axis = 1)
        return IEMGFeature
    
    def MAV(self, ):
        '''
            Mean absolute value(MAV) feature is an aberage of absolute value of the EMG signal amplituden in a segment.
        '''
        MAVFeature = self.IEMG() / self.__DataLen
        return MAVFeature

    def MAV1(self, ):
        '''
            Modified mean absolute value type 1 (MAV1) is an extension of MAV feature. The weighted window function wi is assigned into the equation for improving robustness of MAV feature.
        '''
        MAV1Feature = np.sum(np.abs(self.Data[int(0.25*self.__DataLen) : int(0.75*self.__DataLen)]), axis= 1)
        MAV1Feature = MAV1Feature + np.sum(np.abs(self.Data[ : int(0.25*self.__DataLen)]), axis= 1) * 0.5
        MAV1Feature = MAV1Feature + np.sum(np.abs(self.Data[int(0.75*self.__DataLen) : ]), axis= 1) * 0.5
        return MAV1Feature / self.__DataLen

    def MAV2(self, ):
        '''
            Modified mean absolute value type 2 (MAV2) is an expansion of MAV feature which is similar to the MAV1 Phinyomark. However, the weighted window function wi that s assigned into the equation is a continuous function. It improves smoothness of the weighted function.
        ''' 
        MAV2Feature = np.sum(np.abs(self.Data[int(0.25*self.__DataLen) : int(0.75*self.__DataLen)]), axis= 1)
        for i in range(int(0.25 * self.__DataLen)):
            MAV2Feature += np.abs(self.Data[i]) * (4 * i) / self.__DataLen
        for i in range(int(0.75 * self.__DataLen), self.__DataLen):
            MAV2Feature += np.abs(self.Data[i]) * (4 * (i - self.__DataLen)) / self.__DataLen 
        return MAV2Feature / self.__DataLen
        
    def SSI(self, ):
        '''
            Simple square integral (SSI) or integral square uses energy of the EMG signal as a feature. It is a summation of square values of the EMG signal amplitude. Generally, this parameter is defined as an energy index.
        '''
        SSIFeature = np.sum(np.power(self.Data, 2), axis= 1)
        return SSIFeature

    def VAR(self, ):
        '''
            variance is defined as an average of square values of the deviation of that variable.
        '''
        VARFeature = self.SSI / (self.__DataLen - 1)
        return VARFeature

    def TM_N(self, N):
        '''
            Temporal moment is a statistical analysis. the absolute value was taken to greatly reduce the within class separation for the odd moment case.

            args:
                N: Order number
        '''
        TMFeature = np.sum(np.power(self.Data, N), axis= 1) / self.__DataLen
        return TMFeature
    
    def RMS(self, ):
        '''
            Root mean square (RMS) is another popular feature in analysis of the EMG signal. It is also similar to standard deviation method.
        '''
        return np.power(self.SSI, 0.5)
    
    def V(self, ):
        '''
        
        '''
        pass

    def LOG(self, ):
        '''
            Like the V feature, this feature also provides an estimate of the muscle contraction force.
        '''
        LOGFeature = np.exp(np.sum(np.log(np.abs(self.Data)), axis= 1) / self.__DataLen)
        return LOGFeature
    
    def WL(self, ):
        '''
            Like the V feature, this feature also provides an estimate of the muscle contraction force.It is defined as cumulative length of the EMG waveform over the time segment. Some literatures called this feature as wavelength (WAVE).
        '''
        WLFeature = np.sum(np.abs(self.Data[1:self.__DataLen] - self.Data[:(self.__DataLen - 1)]), axis= 1)
        return WLFeature

    def AAC(self, ):
        '''
            Average amplitude change (AAC) is nearly equivalent to WL feature, except that wavelength is averaged. A number of research studies called this feature as difference absolute mean value (DAMV); however, its definition divides WL value by length N minus one.
        '''
        return self.WL() / self.__DataLen

    def DASDV(self, ):
        '''
            Difference absolute standard deviation value (DASDV) is look like RMS feature, in other words, it is a standard deviation value of the wavelength.        
        '''

        WL_2 = np.sum(np.power((self.Data[1:self.__DataLen] - self.Data[:(self.__DataLen - 1)]), 2), axis= 1)
        DASDVFeature = np.power((WL_2 / (self.__DataLen - 1)), 0.5)
        return DASDVFeature
    
    def ZC(self, threshold = 0):
        '''
            Zero crossing (ZC) is a measure of frequency information of the EMG signal that is defined in time domain. It is a number of times that amplitude values of the EMG signal cross zero amplitude level. To avoid lowvoltage fluctuations or background noises, threshold condition is implemented.

            args:
                threshold: Numerical boundary, The default value of 0.
        '''
        pass

    def MYOP(self, threshold = 0):
        '''
            Myopulse percentage rate (MYOP) is an average value of myopulse output which is defined as one when absolute value of the EMG signal exceeds a pre-defined threshold value.

            args:
                threshold: Numerical boundary, The default value of 0.
        '''
        MYOPFeature = np.zeros(self.Data.shape[1])
        count_EMG_matrix = self.Data >= threshold
        for i in range(len(MYOPFeature)):
            MYOPFeature[i] = count_EMG_matrix[:,i].count(True)
        return MYOPFeature  / self.__DataLen

    def WAMP(self, threshold = 0):
        '''
            Willison amplitude or Wilson amplitude (WAMP) is a measure of frequency information of the EMG signal as same as defines in ZC feature. It is a number of times resulting from difference between the EMG signal amplitude among two adjoining segments that exceeds a pre-defined threshold.
   
            args:
                threshold: Numerical boundary, The default value of 0.
        '''
        WAMPFeature = np.zeros(self.Data[1])
        count__EMG_matrix = (self.Data[: (self.__DataLen - 1)] - self.Data[1:]) >= threshold
        for i in range(len(WAMPFeature)):
            WAMPFeature[i] = count__EMG_matrix[:,i].count(True)
        return WAMPFeature

    def SSC(self, threshold = 0):
        '''
            Slope sign change (SSC) is related to ZC, MYOP, and WAMP features. It is another method to represent frequency information of the EMG signal. It is a number of times that slope of the EMG signal changes sign. The number of changes between the positive and negative slopes among three sequential segments is performed with the threshold function for avoiding background noise in the EMG signal.
   
            args:
                threshold: Numerical boundary, The default value of 0.
        '''
        SSCFeature = np.zeros(self.Data.shape[1])
        count_EMG_matrix = np.zeros(self.Data.shape)
        for i in range(1, self.__DataLen - 1):
            count_EMG_matrix[i] = (self.Data[i] - self.Data[i-1]) * (self.Data[i] - self.Data[i+1])
        count_EMG_matrix = count_EMG_matrix[1: (self.__DataLen - 1)] >= threshold
        for i in range(len(SSCFeature)):
            SSCFeature[i] = count_EMG_matrix[:, i].count(True)
        return SSCFeature
    
    def MAVSLP(self, K = 3):
        '''
            Mean absolute value slope (MAVSLP) is a modified version of MAV feature to establish multiple features. Differences between MAVs of the adjacent segments are determined.

            args:
                K: is number of segments covering the EMG signal, The default value of 3.
        '''
        MAVSLPFeature = np.zeros((K-1, self.Data.shape[1]))
        segment = self.__DataLen / K
        for i in range(K-1):
            MAVSLPFeature[i] = (np.sum(np.abs(self.Data[int((i + 1) * segment) : int((i + 2) * segment)]), axis= 1) - np.sum(np.abs(self.Data[int(i * segment) : int((i + 1) * segment)]), axis= 1)) / segment
        return MAVSLPFeature

    def MHW(self, ):
        '''
        
        '''
        pass

    def MTW(self, ):
        '''
        
        '''
        pass

    def HIST(self, ):
        '''
        
        '''
        pass

    def AR(self, ):
        '''
        
        '''
        pass

    def CC(self, ):
        '''
        
        '''
        pass

    def getFeature(self, FeatureType, **kwargs):
        '''
            Return EMG data feature.

            args:
                threshold: Numerical boundary, The default value of 0.
                K: is number of segments covering the EMG signal, The default value of 3.
                N: Order number
        '''
        ZC_threshold = kwargs.pop("ZC_threshold", 0)
        MYOP_threshold = kwargs.pop("MYOP_threshold", 0)
        WAMP_threshold = kwargs.pop("WAMP_threshold", 0)
        SSC_threshold = kwargs.pop("SSC_threshold", 0)
        K = kwargs.pop("k", 3)
        N = kwargs.pop("N", 0)
        if FeatureType == 'IEMG':
            return self.IEMG
        elif FeatureType == "MAV":
            return self.MAV
        elif FeatureType == "MAV1":
            return self.MAV1
        elif FeatureType == "MAV2":
            return self.MAV2
        elif FeatureType == "SSI":
            return self.SSI
        elif FeatureType == "VAR":
            return self.VAR
        elif FeatureType == "TM_N":
            return self.TM_N(N)
        elif FeatureType == "RMS":
            return self.RMS
        elif FeatureType == "V":
            return self.V
        elif FeatureType == "LOG":
            return self.LOG
        elif FeatureType == "WL":
            return self.WL
        elif FeatureType == "AAC":
            return self.AAC
        elif FeatureType == "DASDV":
            return self.DASDV
        elif FeatureType == "ZC":
            return self.ZC(ZC_threshold)
        elif FeatureType == "MYOP":
            return self.MYOP(MYOP_threshold)
        elif FeatureType == "WAMP":
            return self.WAMP(WAMP_threshold)
        elif FeatureType == "SSC":
            return self.SSC(SSC_threshold)
        elif FeatureType == "MAVSLP":
            return self.MAVSLP(K)
        elif FeatureType == "MHW":
            return self.MHW
        elif FeatureType == "MTW":
            return self.MTW
        elif FeatureType == "HIST":
            return self.HIST
        elif FeatureType == "AR":
            return self.AR
        elif FeatureType == "CC":
            return self.CC
        else:
            return TypeError("Not this type Feature!!")

        



