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
    video_path = "D:/张江涛/手势数据集/手语识别多模态数据/videos/seg_Video_Skeleton/Seg_Video/"
    ske_path = "D:/张江涛/手势数据集/手语识别多模态数据/videos/seg_Video_Skeleton/Seg_Skeleton/"
    MatchingVideoAndSkeleton(video_path, ske_path)
    MatchingVideoAndSkeleton(ske_path, video_path)

    KeyFramePath = "D:/张江涛/手势数据集/手语识别多模态数据/videos/seg_Video_Skeleton/Key_Frame/"
    CheckKeyFrameNum(KeyFramePath)
