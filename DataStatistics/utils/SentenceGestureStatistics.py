'''
Function: Perform statistics on the dataset.
Author: ZhangJiangtao-0108
'''
import os 


class SentenceGestureStatistics():
    '''
        Perform statistics on the dataset.
        DataPath: Dataset path.
    '''
    def __init__(self, DataPath):
        self.DataPath = DataPath
        self.fuhao = ',\!?。，？！、 '

    def SentenceStatistics(self) -> dict:
        '''
            Counting the number of sentences in the dataset.
        '''
        Sentences = []
        SentenceStatisticsDic = {}
        for fname in os.listdir(self.DataPath):
            for x in self.fuhao:
                if x in fname:
                    fname = fname.replace(x,'')
            sentence = fname.split("_")[0].replace('-','')
            Sentences.append(sentence)
        Sentences_set = set(Sentences)
        for sentence in Sentences_set:
            SentenceStatisticsDic[sentence] = Sentences.count(sentence)
        return SentenceStatisticsDic

    def GestureStatistics(self, ) -> dict:
        '''
            Counting the number of gesturess in the dataset.
        '''
        Gestures = []
        GestureStatisticsDic = {}
        for fname in os.listdir(self.DataPath):
            for x in self.fuhao:
                if x in fname:
                    fname = fname.replace(x,'')
            sentence = fname.split("_")[0].split('-')
            for gesture in sentence:
                Gestures.append(gesture)
        Gestures_set = set(Gestures)
        for gesture in Gestures_set:
            GestureStatisticsDic[gesture] = Gestures.count(gesture)
        return GestureStatisticsDic

    def GenerateGestureDic(self,) -> dict:
        '''
            Generate a gesture dictionary.
        '''
        Gestures = []
        for fname in os.listdir(self.DataPath):
            for x in self.fuhao:
                if x in fname:
                    fname = fname.replace(x,'')
            sentence = fname.split("_")[0].split('-')
            for gesture in sentence:
                if gesture not in Gestures:
                    Gestures.append(gesture)
        Gestures += ['sos','eos','pos']
        GestureDic = dict(zip(Gestures, [i for i in range(len(Gestures))])) 
        return GestureDic
        
       

if __name__ == "__main__":
    A = SentenceGestureStatistics("D:/张江涛/手势数据集/手语翻译数据集/emg/")
    print(A.GenerateGestureDic())


