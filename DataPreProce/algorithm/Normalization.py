import numpy as np


class Normalization():
    def __init__(self,):
        pass

    def MaxMinNorm(self, emg, imu, axis:int=0):
        emg_max = emg.max(axis = axis)
        emg_min = emg.min(axis = axis)
        imu_max = imu.max(axis = axis)
        imu_min = imu.min(axis = axis)
        if axis == 0:
            emg_norm = (emg - emg_min)/(emg_max - emg_min)
            imu_norm = (imu - imu_min)/(imu_max - imu_min)
            return emg_norm, imu_norm
        elif axis == 1:
            emg_norm = (emg.T - emg_min)/(emg_max - emg_min)
            imu_norm = (imu.T - imu_min)/(imu_max - imu_min)
            return emg_norm.T, imu_norm.T
        else:
            raise("error")

