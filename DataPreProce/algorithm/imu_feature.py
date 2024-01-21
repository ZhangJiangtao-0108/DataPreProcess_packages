'''
    提取IMU信号的特征
'''
import numpy as np
from  scipy import signal
from algorithm.Attitude_Angle_solution import data_change
from algorithm.imu_position_rotation import Computer_Pos_Roa


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
    
    def POS_ROA(self, Deta= 0.02):
        '''
            Calculate the position and rotation value of each time.
            Deta:interval time
        '''
        data_len = len(self.Data)
        Positions, Rotations = Computer_Pos_Roa(self.Data, Deta)
        Rotations = Rotations.reshape(data_len, -1)
        return np.concatenate((Positions, Rotations), axis = -1)
    
    def QUAT(self,):
        '''
            Calculate the QUAT value of each dimension.
        '''
        return self.Data[:, :4]

    def getFeature(self, FeatureType, **kwargs):
        '''
            Returen IMU data feature.

            args:
                FeatureType:Selected feature types,['EULERANGLE', 'MEAN', 'SUM', 'VAR', 'STD']
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
        elif FeatureType == "POS&ROA":
            return self.POS_ROA()
        elif FeatureType == "QUAT":
            return self.QUAT()
        else:
            raise TypeError("Not " + FeatureType + " Feature!!")
