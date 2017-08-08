import math
from textblob import TextBlob as tb

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

document1 = tb("""
Queen to receive £6m pay increase from public funds
The Sovereign Grant, which pays for the salaries of
her household, official travel and upkeep of palaces, is to increase
by more than £6m in 2018/19.
It comes as accounts revealed the Queen's official net expenditure
last year increased by £2m, to almost £42m. Sir Alan Reid, Keeper of
the Privy Purse, said the Queen represented "excellent value for money".""")
   
document2 = tb("""Python, from the Greek word (πύθων/πύθωνας), is a genus of
nonvenomous pythons[2] found in Africa and Asia. Currently, 7 species are
recognised.[2] A member of this genus, P. reticulatus, is among the longest
snakes known.""")

document3 = tb("""The Colt Python is a .357 Magnum caliber revolver formerly
manufactured by Colt's Manufacturing Company of Hartford, Connecticut.
It is sometimes referred to as a "Combat Magnum".[1] It was first introduced
in 1955, the same year as Smith & Wesson's M29 .44 Magnum. The now discontinued
Colt Python targeted the premium revolver market segment. Some firearm
collectors and writers such as Jeff Cooper, Ian V. Hogg, Chuck Hawks, Leroy
Thompson, Renee Smeets and Martin Dougherty have described the Python as the
finest production revolver ever made.""")


doc = tb(""" 
   
    Dr Yalda Jamshidi, a reader in genomic medicine at 
    St George's University of London, said: "The study is the first to show successful and efficient 
    correction of a disease-causing mutation in early stage human embryos with gene editing.
    The study has already been condemned by Dr David King, from the campaign group Human 
    Genetics Alert, which described the research as "irresponsible" and a "race for first 
    genetically modified baby".
    Dr Shoukhrat Mitalipov, a key figure in the research team, said: "Every generation on would carry 
    this repair because we've removed the disease-causing gene variant from that family's lineage.
 
""")

def get_KWs(text):
    doc = tb(text)
    kw =[]
    bloblist = [doc]
    for i, blob in enumerate(bloblist):
        print("Top words in document {}".format(i + 1))
        scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words[:5]:
            kw.append(word)


          #  print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))
    return kw

"""
bloblist = [document1, document2, document3, doc]
for i, blob in enumerate(bloblist):
    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:5]:
        print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))
"""
