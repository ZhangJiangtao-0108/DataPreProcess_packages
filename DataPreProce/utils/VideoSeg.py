import cv2
from tqdm import tqdm
import os
import numpy as np
import matplotlib.pyplot as plt


class FindSegSections():
    def __init__(self, Steps, Thresholds, D, SegLen = 5, bodyPoints= [3, 4, 6, 7] ):
        self.SegLen = SegLen
        self.bodyPoints = bodyPoints
        self.Steps = Steps
        self.Thresholds = Thresholds
        self.D = D
    
    def _FindFrameDiff(self,):
        ### 寻找骨骼点的变化情况
        self.diff = []
        for i in range(len(self.subsets)):
            sum = 0
            for j in self.bodyPoints:
                index1 = int(self.subsets[i][0][j])
                index2 = int(self.subsets[10][0][j])
                count = 1
                if index1 != -1 and index2 != -1:
                    # sum +=  self.bodyLadmarks[i+1][index2][0:2] - self.bodyLadmarks[i][index1][0:2]
                    sum +=  self.bodyLadmarks[i][index1][0:2] - self.bodyLadmarks[10][index2][0:2]
                    count += 1
            self.diff.append(np.sum(sum) / count)


    def FindSegSets(self, step, Threshold, d: int):
        '''
            根据前后帧的动作变化来决定（目前尚未完善）
        '''
        ## 寻找视频分割区区间
        SegSection = []
        P_Start, P_End, State_Start,  State_End = 0, 0, False, False
        State = False
        i = step
        while i <= len(self.diff)-step:
            F = np.abs(self.diff)[i-step:i]
            B = np.abs(self.diff)[i:i+step]
            if State == False:
                if np.sum(F<Threshold) > (step-1) and np.sum(B>Threshold) > (step-d) and State_Start == False:
                    P_Start = i
                    State_Start = True
                    State = True
            else:
                if np.sum(B<Threshold) > (step-1) and np.sum(F>Threshold) > (step-d) and State_End == False:
                    P_End = i
                    State_End = True
                    State = True
            if State_Start == True and State_End == True:
                SegSection.append([P_Start, P_End])
                State_Start = False
                State_End = False
                State = False
            i += 1
        return SegSection

    def SegSectionCorr(self, SegSection):
        '''
            对分割区间进行纠正
        '''
        # SegLen = [SegSection[i][1] - SegSection[i][0] for i in range(len(SegSection))]
        SegGap = [SegSection[i][0] - SegSection[i-1][1] for i in range(1,len(SegSection))]
        for i in range(1, len(SegSection)-1):
            Gap_F = SegSection[i][0] - SegSection[i-1][1]
            Gap_B = SegSection[i+1][0] - SegSection[i][1]
            if (Gap_F < 40 or Gap_F > 110) and (Gap_B > 110 or Gap_B < 40): 
                SegSection[i][0] = int((SegSection[i+1][0] + SegSection[i-1][1]) / 2  - (SegSection[i][1] - SegSection[i][0])/2)
                SegSection[i][1] = int((SegSection[i+1][0] + SegSection[i-1][1]) / 2  + (SegSection[i][1] - SegSection[i][0])/2)
        return SegSection

    def DecSegSection(self, ):
        SegSections = []
        ## 寻找于初始位置骨骼点的差值
        self._FindFrameDiff()
        ## 寻找可能区间
        for step in self.Steps:
            for Threshold in self.Thresholds:
                for d in self.D:
                    if step - d >= 6:
                        SegSection = self.FindSegSets(step, Threshold, d)
                        if len(SegSection) == self.SegLen:
                            SegSections.append(SegSection)
        ## 决定最终区间
        SegSections = np.array(SegSections)
        # print(SegSections)
        FinalSegSection = []
        if np.any(SegSections):
            ## 决定初始化区间
            for i in range(5):
                left_min_temp = int(np.min(SegSections[:,i, 0],axis = 0))
                left_max_temp = int(np.max(SegSections[:,i, 0],axis = 0))
                left_mean_temp = int(np.mean(SegSections[:,i, 0],axis = 0))
                right_min_temp = int(np.min(SegSections[:,i, 1],axis = 0))
                right_max_temp = int(np.max(SegSections[:,i, 1],axis = 0))
                right_mean_temp = int(np.mean(SegSections[:,i, 1],axis = 0))
                left_bound = int(left_min_temp + (left_mean_temp - left_min_temp) * 0.1)
                right_bound = int(right_max_temp - (right_max_temp - right_mean_temp) * 0.1)
                # if (right_bound - left_bound) < 80:
                #     left_bound = left_mean_temp - 40
                #     right_bound = left_mean_temp + 40
                FinalSegSection.append([left_bound, right_bound])
            ## 对区间进行纠正
            for i in range(len(FinalSegSection)-1):
                if (FinalSegSection[i+1][0] -  FinalSegSection[i][1]) < 0:
                    FinalSegSection = []
                    break
            # FinalSegSection = self.SegSectionCorr(FinalSegSection)
        # print(FinalSegSection)
        
        return FinalSegSection

    def GetSegSections(self, subsets, bodyLadmarks):
        self.subsets = subsets
        self.bodyLadmarks = bodyLadmarks
        FinalSegSection = self.DecSegSection()
        return FinalSegSection

def SegSkeleton(skeleton, SavePath, SegSection, BodySection):
    filename = SavePath.split("/")[-1] 
    bodyLadmarks = skeleton["bodyLandmarks"]
    handLandmarks = skeleton["handLandmarks"]
    ## 对骨骼点进行修正
    for i in range(len(bodyLadmarks)):
        bodyLadmarks[i][:,0] = bodyLadmarks[i][:, 0] -  BodySection[0]
        for j in range(len(handLandmarks[i])):
            handLandmarks[i][j][:, 0] = np.maximum(handLandmarks[i][j][:, 0] - BodySection[0], 0)
    for i in range(len(SegSection)):
        result_file  = SavePath+ "_" + str(i+1) + "/" + filename + "_" + str(i+1) + ".npz"
        np.savez(result_file, subsets = skeleton["subsets"][SegSection[i][0]:SegSection[i][1]], bodyLandmarks = bodyLadmarks[SegSection[i][0]:SegSection[i][1]], handLandmarks = handLandmarks[SegSection[i][0]:SegSection[i][1]])
    

def SegVideo(Video, SavePath, SegSection, BodySection):
    ## 获取视频名称
    video_name = Video.split("/")[-1].split('.')[0]

    cap = cv2.VideoCapture(Video)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 用于mp4格式的生成的参数
    fps = cap.get(cv2.CAP_PROP_FPS)  # fps = int(cap.get(cv2.CAP_PROP_FPS)) 获取视频帧数，或者自己写
    # weight = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 获取视频宽，或者自己写
    weight = int(BodySection[1] - BodySection[0])  # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 获取视频宽，或者自己写
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
            # if ret:
            newframe = frame[ :,BodySection[0]:BodySection[1]]
            cv2.imwrite(filefolder + "/" + str(int(pos-start)) + ".jpg",newframe)  # 利用'写入视频对象'写入帧
            videowriter.write(newframe)  # 保存成对应的视频
            pos = cap.get(cv2.CAP_PROP_POS_FRAMES)  # 获取当前帧数pos
            cv2.waitKey(1)
        videowriter.release()
    cap.release()  # 关闭读取视频对象

def StartSegVedios(Filenames, PathKwargs, ParametersKwargs):
    Video_path = PathKwargs["Video_path"]
    npz_Path = PathKwargs["npz_Path"]
    Save_Path = PathKwargs["Save_Path"]
    SegRes_Path = PathKwargs["SegRes_Path"]
    if not os.path.exists(SegRes_Path):
        os.mkdir(SegRes_Path)
    if not os.path.exists(Save_Path):
        os.mkdir(Save_Path)
    
    Steps = ParametersKwargs["Steps"]
    Thresholds = ParametersKwargs["Thresholds"]
    D = ParametersKwargs["D"]
    FinSegTool = FindSegSections(Steps, Thresholds, D)

    ## 记录出错文件
    SegErrorFiles = []
    ErrorFiles = []             
    
    for filename, _ in zip(Filenames, tqdm(range(len(Filenames)))):
        ## 加载骨骼点
        # Skeletal point extraction using the open source OpenPose algorithm, obtained at: 
        # https://github.com/Hzzone/pytorch-openpose
        skeleton_file = npz_Path + filename
        skeleton = np.load(skeleton_file, allow_pickle=True)
        subsets = skeleton["subsets"]
        bodyLadmarks = skeleton["bodyLandmarks"]
        handLandmarks = skeleton["handLandmarks"]
        try:
            ## 人物区间范围
            body_max = 0
            body_min = 1000
            for i in range(len(bodyLadmarks)):
                # print(bodyLadmarks[i].shape)
                # print(np.amax(bodyLadmarks[i], axis=0)[0])
                if np.amax(bodyLadmarks[i], axis=0)[0] > body_max :
                    body_max = np.amax(bodyLadmarks[i], axis=0)[0]
                if np.amin(bodyLadmarks[i], axis=0)[0] < body_min :
                    body_min = np.amin(bodyLadmarks[i], axis=0)[0]
            
            BodySection = [int(body_min-20), int(body_max+20)]
            # print(len(BodySection))
            
            ## 获取分割区间
            SegSection = FinSegTool.GetSegSections(subsets, bodyLadmarks)
            if len(SegSection) != 5:
                raise SegError("分割个数不正确")

            ## 分割视频
            Video = Video_path + filename.split(".")[0] + ".mp4"
            SegVideo(Video, Save_Path, SegSection, BodySection)

            ## 保存对应的骨骼信息
            SkeletionPath = Save_Path + filename.split(".")[0]
            SegSkeleton(skeleton, SkeletionPath, SegSection, BodySection)

            ## 保存分割结果
            with open(SegRes_Path + filename.split(".")[0] + ".txt","w") as SegFile:
                print(SegSection, file= SegFile)
        except (IndexError, ValueError, TypeError):
            if filename not in ErrorFiles:
                ErrorFiles.append(filename)
        except SegError:
            if filename not in SegErrorFiles:
                SegErrorFiles.append(filename)
    return SegErrorFiles, ErrorFiles


class SegError(Exception):
    pass
        

if __name__ == "__main__":
    PathKwargs = {
        "Video_path":"D:/张江涛/手势数据集/手语识别多模态数据/videos/sort2Siger/张江涛/", 
        "npz_Path":"D:/张江涛/手势数据集/手语识别多模态数据/videos/skeleton/zhangjiangtao_npz/",
        "Save_Path":"D:/张江涛/手势数据集/手语识别多模态数据/videos/segVideo/张江涛/",
        "SegRes_Path":"D:/张江涛/手势数据集/手语识别多模态数据/videos/segVideo/张江涛_Seg/",
    }

    '''
    Filenames = os.listdir(PathKwargs["npz_Path"])
    ## 第一次分割
    ParametersKwargs = {
        "Steps":[int(i) for i in range(10, 16)],
        "Thresholds":[int(i*5) for i in range(6,11)],
        "D":[int(i) for i in range(4,9) ],
    }
    
    SegErrorFiles, ErrorFiles = StartSegVedios(Filenames, PathKwargs, ParametersKwargs)

    with open(PathKwargs["Video_path"] + "ErrorFiles.txt",'w') as f:
        for filename in ErrorFiles:
            print(filename, file=f)
    with open(PathKwargs["Video_path"] + "SegErrorFiles.txt",'w') as f_:
        for filename in SegErrorFiles:
            print(filename, file=f_)
    '''

    ## 进行多次分割
    Filenames = []
    f = open(PathKwargs["Video_path"] + "SegErrorFiles.txt",'r')
    for line in f.readlines():
        Filenames.append(line.replace("\n", ""))
    f.close()
    # print(Filenames)
    ParametersKwargs = {
        "Steps":[int(i) for i in range(16, 20)],
        "Thresholds":[int(i*5) for i in range(4,6)],
        "D":[int(i) for i in range(9,12)],
    }
    SegErrorFiles, ErrorFiles = StartSegVedios(Filenames, PathKwargs, ParametersKwargs)
    # print(SegErrorFiles)
    # print(ErrorFiles)
    with open(PathKwargs["Video_path"] + "SegErrorFiles.txt",'w') as f_:
        for filename in SegErrorFiles:
            print(filename, file=f_)


