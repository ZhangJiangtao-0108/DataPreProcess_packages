'''
    提取IMU信号的特征
'''
import numpy as np
from  scipy import signal
from algorithm.Attitude_Angle_solution import data_change



class IMUDataFeature():
    def __init__(self, Data) -> None:
        self.Data = Data
        self.__DataLen__ = len(self.Data)

    def EulerAngle(self, ):
        '''
            Calculation of Euler angles from acceleration and angular velocity data of IMU.
        '''
        pitch, roll, yaw = data_change(self.Data)
        
        return np.vstack((pitch, roll, yaw))

    def Mean(self,):
        '''
            Calculate the mean value of each dimension.
        '''
        return np.mean(self.Data, axis= 0)

    def Sum(self, ):
        '''
            Calculate the sum value of each dimension.
        '''
        return np.sum(self.Data, axis= 0)

    def Var(self, ):
        '''
            Calculate the var value of each dimension.
        '''
        return np.var(self.Data, axis= 0)

    def Std(self, ):
        '''
            Calculate the std value of each dimension.
        '''
        return np.std(self.Data, axis= 0)

    def getFeature(self, FeatureType, **kwargs):
        '''
            Returen IMU data feature.

            args:

        '''
        if FeatureType == 'EULERANGLE':
            return self.EulerAngle()
        elif FeatureType == "MEAN":
            return self.Mean()
        elif FeatureType == "SUM":
            return self.Sum()
        elif FeatureType == "VAR":
            return self.Var()
        elif FeatureType == "STD":
            return self.Std()
        else:
            raise TypeError("Not " + FeatureType + " Feature!!")
