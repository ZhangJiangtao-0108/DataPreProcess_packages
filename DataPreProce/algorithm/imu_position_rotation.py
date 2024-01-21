import math
import numpy as np

def Computer_rotation(x_ang=0, y_ang=0, z_ang=0, deta=0.02):
    '''从imu数据中计算当前时刻的偏转量
        x_ang:x轴上的角速度
        y_ang:y轴上的角速度
        z_ang:z轴上的角速度
    '''
    R = np.zeros((3,3))
    x_c, x_s = math.cos(deta * x_ang), math.sin(deta * x_ang)
    y_c, y_s = math.cos(deta * y_ang), math.sin(deta * y_ang)
    z_c, z_s = math.cos(deta * z_ang), math.sin(deta * z_ang)
    R[0,0] = y_c * z_c
    R[0,1] = x_s * y_s * z_c - x_c * z_s
    R[0,2] = x_c * y_s * z_c + x_s * z_s
    R[1,0] = y_c * z_s
    R[1,1] = x_s * y_s * z_s + x_c * z_c
    R[1,2] = x_c * y_s * z_s - x_s * z_c
    R[2,0] = -y_s
    R[2,1] = x_s * y_c
    R[2,2] = x_c * y_c
    return np.array(R)

def Computer_position(x_acc, y_acc, z_acc, initial_position=[0,0,0], R=None, deta=0.02):
    '''从imu数据中计算当前时刻的位置
        initial_position:初始位置
        x_acc:x轴上的加速度
        y_acc:y轴上的加速度
        z_acc:z轴上的加速度
        R:当前时刻的旋转矩阵
    '''
    position = np.zeros(3)
    x_sum, y_sum, z_sum = 0, 0, 0
    for i in range(len(x_acc)):
        x_sum += x_acc[i] * deta
        y_sum += y_acc[i] * deta
        z_sum += z_acc[i] * deta
    position[0] = initial_position[0] + x_sum * deta
    position[1] = initial_position[1] + y_sum * deta
    position[2] = initial_position[2] + z_sum * deta
    # print(R)
    # print(position)
    # print(np.matmul(position * R ))
    position = np.matmul(position, R )
    return position

def Computer_Pos_Roa(imu_data, Deta = 0.02):
    '''
    imu_data:[imu_dim_1, imu_dim_2]
    Deta:时间间隔

    '''
    X_acc = imu_data[:, 4]
    Y_acc = imu_data[:, 5]
    Z_acc = imu_data[:, 6]

    X_ang = imu_data[:, 7]
    Y_ang = imu_data[:, 8]
    Z_ang = imu_data[:, 9]

    Positions = []
    Rotations = []
    position = np.array([0,0,0])
    for i in range(len(imu_data)):
        R = Computer_rotation(X_ang[i], Y_ang[i], Z_ang[i],Deta)
        position = Computer_position(X_acc[:i], Y_acc[:i], Z_acc[:i], position,R, Deta)
        Rotations.append(R)
        Positions.append(position)

    Positions = np.array(Positions)
    Rotations = np.array(Rotations)

    # print(Positions.shape)
    # print(Rotations.shape)

    return Positions, Rotations


    
