## 数据预处理的包
# __init.py
'''
    可以在这个文件中批量导入所需要的模块
'''
import numpy as np
import os
import DataPre

__all__ = ["DataPre",\
            "makedatasets",\
            "algorithm.Attitude_Angle_solution",\
            "algorithm.cutting_algorithm",\
            "algorithm.emg_correct",\
            "algorithm.emg_feature"]
