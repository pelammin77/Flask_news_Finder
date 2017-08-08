"""
file: text simylarity.py
author: Petri Lamminaho 



"""

import re
import math
from collections import Counter
import nltk


WRD = re.compile(r'\w+')


def is_same_text(t1, t2, cos):
    res = compare_texts(t1.lower(), t2.lower())
    #print(cos)
    #print(res)
    if res*100 > cos:
        return True
    else:
        return False


def compare_texts(t1, t2):
    vector1 = text_to_vector(t1)
    vector2 = text_to_vector(t2)
    cosine = get_cos(vector1, vector2)
    return cosine
    #print('cosine', cosine)


# calculates two vectors similarity (cosine similarity)
def get_cos(vect1, vect2):
    inter = set(vect1.keys())& set(vect2.keys())
    num = sum([vect1[x] * vect2[x] for x in inter])

    sum1 = sum([vect1[x]**2 for x in vect1.keys()])
    sum2 = sum([vect2[x]**2 for x in vect2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        0.0
    else:
        return float(num)/ denominator

# converts text to vector
def text_to_vector(text):
    words = WRD.findall(text)
    return Counter(words)

# Gets sen post tag
def get_tags(sen, tag='NNP'):

    tagged_sent = nltk.pos_tag(sen.split())
    propernouns = [word for word, pos in tagged_sent if pos == tag]
    print(propernouns)


def search_text(key_text, seach_line):
    seach_result = re.search(key_text, seach_line, re.M|re.I)
    if seach_result:
        print("Text " + seach_result.group() + " found")
    else:
        print("Text not found")



# Test/main
"""
text1 = "White House communications director quits"
text2 = 'White House communications director Mike Dubke is leaving the administration, ' \
        'he said Tuesday, amid swirling speculation about a possible Trump staff shakeup.'
text3 = 'Putin meets Trump'
text4 = 'Trump meets Putin'
text5 = 'Trump is Russian spy'
text6 = "Supreme Court allows limited version of Trump’s travel ban to take effect and will consider case in fall"
text7 = "Supreme Court to Hear Travel Ban Case"
text8 = "supreme court  travel ban"
text9 = 'Travel Ban Supreme Court'

res = compare_texts(text9.lower(), text6.lower())
print("Text simularity is", res*100,'%')
"""




#get_tags(text1)
#get_tags(text2)

