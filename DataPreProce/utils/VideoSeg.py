import cv2
from tqdm import tqdm
import os
import numpy as np


def FindSegSets(subsets, bodyLadmarks):
    ## 寻找视频分割区区间
    SegSection = []
    ### 寻找骨骼点的变化情况
    diff = []
    bodyPoints = [3, 4, 6, 7]
    for i in range(len(subsets)-1):
        sum = 0
        for j in bodyPoints:
            index1 = int(subsets[i][0][j])
            index2 = int(subsets[i+1][0][j])
            count = 0
            if index1 != -1 and index2 != -1:
                sum +=  bodyLadmarks[i+1][index2][0:2] - bodyLadmarks[i][index1][0:2]
                count += 1
        diff.append(np.sum(sum) / count)

    P_Start, P_End, State_Start,  State_End = 0, 0, False, False
    State = False
    step = 15
    Threshold = 10
    i = step
    while i <= len(diff)-step:
        F = np.abs(diff)[i-step:i]
        B = np.abs(diff)[i:i+step]
        if State == False:
            if np.sum(F<Threshold) > (step-2) and np.sum(B>Threshold) > (step-7) and State_Start == False:
                P_Start = i
                State_Start = True
                State = True
        else:
            if np.sum(B<Threshold) > (step-2) and np.sum(F>Threshold) > (step-7) and State_End == False:
                P_End = i
                State_End = True
                State = True
        if State_Start == True and State_End == True:
            SegSection.append([P_Start, P_End])
            State_Start = False
            State_End = False
            State = False
        i += 1

    print(SegSection)

    return SegSection


def SegVideo(Video, SavePath, SegSection):
    ## 获取视频名称
    video_name = Video.split("/")[-1].split('.')[0]

    cap = cv2.VideoCapture(Video)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 用于mp4格式的生成的参数
    fps = cap.get(cv2.CAP_PROP_FPS)  # fps = int(cap.get(cv2.CAP_PROP_FPS)) 获取视频帧数，或者自己写
    weight = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 获取视频宽，或者自己写
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 获取视频长，或者自己写

    ## 获取视频帧
    for num in range(len(SegSection)):
        filefolder = SavePath  +   video_name + "_" + str(num+1)
        output = filefolder + "/" + video_name + "_" + str(num+1) + ".mp4"
        if os.path.exists(filefolder) == False:
            os.mkdir(filefolder)

        videowriter = cv2.VideoWriter(output, fourcc, fps, (int(weight), int(height)))  # 创建一个写入视频对象
        
        start, end = SegSection[num][0], SegSection[num][1]
        cap.set(cv2.CAP_PROP_POS_FRAMES, start)
        pos = cap.get(cv2.CAP_PROP_POS_FRAMES)  # 获取当前帧数
        while pos < end:  # 从start到end之间读取帧数
            ret, frame = cap.read()  # 从开始帧开始读取，之后会从开始帧依次往后读取，直到退出循环
            cv2.imwrite(filefolder + "/" + str(int(pos-start)) + ".jpg",frame)  # 利用'写入视频对象'写入帧
            videowriter.write(frame)  # 保存成对应的视频
            pos = cap.get(cv2.CAP_PROP_POS_FRAMES)  # 获取当前帧数pos
            cv2.waitKey(1)
        videowriter.release()
    cap.release()  # 关闭读取视频对象



if __name__ == "__main__":
    Video_path = "C:/Users/张江涛/Desktop/video/"
    npz_Path = "C:/Users/张江涛/Desktop/npz/"
    Save_Path = "C:/Users/张江涛/Desktop/save/"
    Filenames = os.listdir(npz_Path)
    for filename, _ in zip(Filenames, tqdm(range(len(Filenames)))):
        ## 加载骨骼点
        skeleton_file = npz_Path + filename
        skeleton = np.load(skeleton_file, allow_pickle=True)
        subsets = skeleton["subsets"]
        bodyLadmarks = skeleton["bodyLandmarks"]
        ## 获取分割区间
        SegSection = FindSegSets(subsets, bodyLadmarks)
        ## 分割视频
        Video = Video_path + filename.split(".")[0] + ".mp4"
        SegVideo(Video, Save_Path, SegSection)


