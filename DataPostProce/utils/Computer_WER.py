import difflib

def computeWer(str1, str2):
    leven_distance = 0                ## 编辑距离
    s = difflib.SequenceMatcher(None, str1, str2)
    S, I, D = '', '', ''

    for tag, i1, i2, j1, j2 in s.get_opcodes():
        # print('{:7} a[{}: {}] --> b[{}: {}] {} --> {}'.format(tag, i1, i2, j1, j2, str1[i1: i2], str2[j1: j2]))

        if tag == 'replace':
            # print('替换：{}-->{}\t统计个数：{}'.format(str1[i1: i2], str2[j1: j2], max(i2-i1, j2-j1)))
            leven_distance += max(i2-i1, j2-j1)
            S += str1[i1: i2]
        elif tag == 'insert':
            # print('插入：{}-->{}\t统计：{}'.format(str1[i1: i2], str2[j1: j2], j2-j1))
            leven_distance += (j2-j1)
            I += str2[j1: j2]
        elif tag == 'delete':
            # print('删除：{}-->{}\t统计：{}'.format(str1[i1: i2], str2[j1: j2], i2-i1))
            leven_distance += (i2-i1)
            D += str1[i1: i2]
    distance = (len(str1)-leven_distance)/len(str1)
    return S, I, D, distance