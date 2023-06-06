
def SentenceCompare(Template_Sentences_list, Compare_Sentences_list, neglect:list):
    if len(Template_Sentences_list) != len(Compare_Sentences_list):
        raise IndexError("句子条数不匹配")
    
    Template_Gesture_Sta = {}
    Correct_Gesture_sta = {}
    Template_Gestures = []
    Correct_Gestures = []
    for i in range(len(Compare_Sentences_list)):
        Template_Gestures += Template_Sentences_list[i]
        for gesture in Compare_Sentences_list[i]:
            if (gesture not in neglect) and (gesture in Template_Sentences_list[i]):
                Correct_Gestures.append(gesture)
        
    Template_Gestures_set = set(Template_Gestures)
    for gesture in Template_Gestures_set:
        Template_Gesture_Sta[gesture] = Template_Gestures.count(gesture)

    Correct_Gestures_set = set(Correct_Gestures)
    for gesture in Correct_Gestures_set:
        Correct_Gesture_sta[gesture] = Correct_Gestures.count(gesture)

    return Template_Gesture_Sta, Correct_Gesture_sta