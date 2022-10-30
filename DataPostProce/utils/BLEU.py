'''
function:
Author: ZhangJiangtao-0108
'''

## 好像是不需要这个操作
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu, SmoothingFunction
from Labels2Text import Labels2Text

class BLEU():
    '''
    
    '''
    def __init__(self,smoothing_function):
        self.smoothing_function = smoothing_function

    def bleu_score(self, references, candidates):
        '''
        
        '''


