from utils.Computer_WER import computeWer
from utils.Labels2Text import geatures2text
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu


def compute_SLT_Indicators(sentence_candidate_list, Sentence, pre_label):
    '''
        sentence_candidate_list:Spoken句子列表集合[batch_size, candidate_num, sentence_len]
        sentence:句子列表[batch_size, sentence_len]
        pre_label:预测句子列表[batch_size, sentence_len]
    '''
    corpus_bleu_score = corpus_bleu(sentence_candidate_list, pre_label)
    sentence_bleu_score = sentence_bleu(Sentence, pre_label)
    sentence_bleu1_score = sentence_bleu(Sentence, pre_label, weights=(1, 0, 0, 0))
    sentence_bleu2_score = sentence_bleu(Sentence, pre_label, weights=(0, 1, 0, 0))
    sentence_bleu3_score = sentence_bleu(Sentence, pre_label, weights=(0, 0, 1, 0))
    sentence_bleu4_score = sentence_bleu(Sentence, pre_label, weights=(0, 0, 0, 1))
    wer = 0
    for b in range(len(Sentence)):
        _,_,_, WER = computeWer(geatures2text(Sentence[b]), geatures2text(pre_label[b]))
        wer += WER
    wer = wer/len(Sentence)
    return corpus_bleu_score, sentence_bleu_score, sentence_bleu1_score, sentence_bleu2_score, sentence_bleu3_score, sentence_bleu4_score, wer
