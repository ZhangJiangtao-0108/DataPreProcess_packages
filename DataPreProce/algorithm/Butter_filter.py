'''
定义滤波器
'''
from scipy import signal
def butter_filter(data, category = 'lowpass', order = 8, Wn = 0.5, axis = 0):
    '''巴特沃斯低通滤波器

        args:
            category:滤波的形式，lowpass[低通滤波]，highpass[高通滤波]，bandpass[带通滤波]，bandtop[带阻滤波]
            oeder:阶数
            Wn:选择滤波的阈值，其中带通滤波和带阻滤波为一个list
    '''
    b, a = signal.butter(order, Wn, category)   #配置滤波器 8 表示滤波器的阶数
    filtedData = signal.filtfilt(b, a, data, axis=axis)  #data为要过滤的信号
    return filtedData