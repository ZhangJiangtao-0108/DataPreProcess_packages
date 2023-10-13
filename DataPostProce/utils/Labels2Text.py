'''
Function: Turn predictive labels into sentences
Author: ZhangJiangtao-0108
'''
import numpy as np

class Labels2Text():
    '''
        Converting tags into corresponding sentences.
    '''
    def __init__(self,Gesture_dic_path):
        self.Gesture_dic = {}
        self.__getGeatureDic(Gesture_dic_path)

    def labels2gestures(self,labels):
        '''
            Converting labels into corresponding gestures.
        '''
        labels_ = np.array(labels)
        gestures_ = []
        for i in range(len(labels_)):
            gesture = []
            for j in range(len(labels_[i])):
                gesture.append(self.Gesture_dic[labels_[i][j]])
            gestures_.append(gesture)
        return gestures_

    def labels2text(self, labels):
        '''
            Converting tags into corresponding sentences.
        '''
        gestures = self.labels2gestures(labels)
        sentences = []
        for i in range(len(gestures)):
            sentence = ''
            # sentence = geatures2text(gestures[i])
            for word in gestures[i]:
                if word != 'pos' and word != 'eos' and word != 'sos':
                    sentence += word
            sentences.append(sentence)
        return sentences

    def __getGeatureDic(self, Gesture_dic_path):
        '''
            Get geature dic.
        '''
        with open(Gesture_dic_path,'r') as gesture_dic_file:
            self.Gesture_dic_ = eval(gesture_dic_file.readline())
            self.__changeKeyValue()

    def __changeKeyValue(self):
        '''
            Converting the key-value pairs of the gesture dictionary.
        '''
        for gesture in self.Gesture_dic_.keys():
            self.Gesture_dic[self.Gesture_dic_[gesture]] = gesture

def geatures2text(gestures):
    sentence = ''
    for word in gestures:
        if word != 'pos' and word != 'eos' and word != 'sos':
            sentence += word
    return sentence




