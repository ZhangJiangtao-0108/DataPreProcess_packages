'''


'''

import os

def MatchingVideoAndSkeleton(video_path, ske_path):
    videoFiles = os.listdir(video_path)
    skeFiles = os.listdir(ske_path)
    skeList = []
    for skeFile in skeFiles:
        skeList.append(skeFile.split('.')[0])
    # print(skeFile)

    for videoFile in videoFiles:
        if videoFile.split(".")[0] not in skeList:
            print(videoFile)

def CheckKeyFrameNum(KeyFramePath, num = 16):
    KeyFrameNames = os.listdir(KeyFramePath)
    for KeyFrameName in KeyFrameNames:
        FrameNum = len(os.listdir(KeyFramePath + KeyFrameName))
        if FrameNum != num:
            print(KeyFrameName)


if __name__ == "__main__":
    root_Path = "D:/张江涛/手势数据集/手语识别多模态数据/videos/seg_Video_Skeleton/"
    root_Path = "/media/zjt/ZJT/Sign_Language_Recognition_Data/Sign_Multimodal_Data/Video/seg_Video_Skeleton/"
    video_path = root_Path + "Seg_Video/"
    ske_path = root_Path + "Seg_Skeleton/"
    MatchingVideoAndSkeleton(video_path, ske_path)
    MatchingVideoAndSkeleton(ske_path, video_path)

    KeyFramePath = root_Path + "Key_Frame/"
    CheckKeyFrameNum(KeyFramePath)
