from utils.Computer_WER import computeWer
from utils.Labels2Text import geatures2text
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu


def compute_SLT_Indicators(Sentence, pre_label, sentence_candidate_list=None):
    '''
        sentence_candidate_list:Spoken句子列表集合[batch_size, candidate_num, sentence_len]
        sentence:句子列表[batch_size, 1, sentence_len]
        pre_label:预测句子列表[batch_size, sentence_len]
    '''
    
    # print(Sentence)
    # print(pre_label)
    sentence_bleu_score = 0.0
    sentence_bleu1_score = 0.0
    sentence_bleu2_score = 0.0
    sentence_bleu3_score = 0.0
    sentence_bleu4_score = 0.0
    wer = 0.0
    for b in range(len(Sentence)):
        sentence_bleu_score += sentence_bleu([Sentence[b]], pre_label[b])
        sentence_bleu1_score += sentence_bleu([Sentence[b]], pre_label[b], weights=(1, 0, 0, 0))
        sentence_bleu2_score += sentence_bleu([Sentence[b]], pre_label[b], weights=(0, 1, 0, 0))
        sentence_bleu3_score += sentence_bleu([Sentence[b]], pre_label[b], weights=(0, 0, 1, 0))
        sentence_bleu4_score += sentence_bleu([Sentence[b]], pre_label[b], weights=(0, 0, 0, 1))
    
        _,_,_, WER = computeWer(geatures2text(Sentence[b]), geatures2text(pre_label[b]))
        wer += WER
    wer = wer/len(Sentence)
    if sentence_candidate_list != None:
        corpus_bleu_score = corpus_bleu(sentence_candidate_list, pre_label)
        return corpus_bleu_score, sentence_bleu_score, sentence_bleu1_score, sentence_bleu2_score, sentence_bleu3_score, sentence_bleu4_score, wer
    else:
        return sentence_bleu_score, sentence_bleu1_score, sentence_bleu2_score, sentence_bleu3_score, sentence_bleu4_score, wer
