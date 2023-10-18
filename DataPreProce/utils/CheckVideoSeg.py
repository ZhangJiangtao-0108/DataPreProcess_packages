'''


'''

import os

def MatchingVideoAndSkeleton(Tem_path, Check_path, isDel = False):
    '''
    检测文件夹中的数据是否匹配
        Tem_path:模板文件夹
        Check_path:检测的文件夹
        isDel:是否进行文件删除
    '''
    TemFiles = os.listdir(Tem_path)
    CheckFiles = os.listdir(Check_path)
    TemList = []
    for TemFile in TemFiles:
        TemList.append(TemFile.split('.')[0])
    # print(skeFile)

    for CheckFile in CheckFiles:
        if CheckFile.split(".")[0] not in TemList:
            print(CheckFile)
            if isDel:
                os.remove(Check_path + CheckFile)


def CheckKeyFrameNum(KeyFramePath, num = 16,  isDel = False):
    KeyFrameNames = os.listdir(KeyFramePath)
    for KeyFrameName in KeyFrameNames:
        FrameNum = len(os.listdir(KeyFramePath + KeyFrameName))
        if FrameNum != num:
            print(KeyFrameName)
            if isDel:
                os.rmdir(KeyFramePath + KeyFrameName)


if __name__ == "__main__":
    root_Path = "D:/张江涛/手势数据集/手语识别多模态数据/videos/seg_Video_Skeleton/"
    root_Path = "/media/zjt/ZJT/Sign_Language_Recognition_Data/Sign_Multimodal_Data/Video/seg_Video_Skeleton/"
    video_path = root_Path + "Seg_Video/"
    ske_path = root_Path + "Seg_Skeleton/"
    # MatchingVideoAndSkeleton(video_path, ske_path, isDel=True)
    # MatchingVideoAndSkeleton(ske_path, video_path, isDel=True)

    MatchingVideoAndSkeleton(video_path, ske_path)
    MatchingVideoAndSkeleton(ske_path, video_path)

    KeyFramePath = root_Path + "Key_Frame/"
    # CheckKeyFrameNum(KeyFramePath, isDel=True)
    CheckKeyFrameNum(KeyFramePath)

    ## 删除不匹配的文件文件

