"""
file: find_ent.py
author: Petri Lamminaho 
"""
import nltk
from nltk.corpus import stopwords
stopwords = stopwords.words('english')



lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()


"""
# You can use these tags  
###########################################
ORGANIZATION 	Georgia-Pacific Corp., WHO
PERSON 	        Eddy Bonte, President Obama
LOCATION 	    Murray River, Mount Everest
DATE 	        June, 2008-06-29
TIME 	        two fifty a m, 1:30 p.m.
MONEY 	        175 million Canadian Dollars, GBP 10.40
PERCENT 	    twenty pct, 18.75 %
FACILITY 	    Washington Monument, Stonehenge
GPE 	       South East Asia, Midlothian
############################################
"""

sentence_re = r'''(?x)      # set flag to allow verbose regexps
      ([A-Z])(\.[A-Z])+\.?  # abbreviations, e.g. U.S.A.
    | \w+(-\w+)*            # words with optional internal hyphens
    | \$?\d+(\.\d+)?%?      # currency and percentages, e.g. $12.40, 82%
    | \.\.\.                # ellipsis
    | [][.,;"'?():-_`]      # these are separate tokens
'''


""""
grammar = "NP: {<DT>?<JJ>*<NN>}"
chunkGram = r"""#Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
"""chunk_parser = nltk.RegexpParser(chunkGram)
print(chunk_parser, "parser")
def make_chunk(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    cp = nltk.RegexpParser(chunkGram)
   # chunk_parser = nltk.RegexpParser(chunkGram)
    chunged = chunk_parser.parse(pos)
    print(chunged)
    #chunged.draw()






def leaves(tree):
    #Finds NP (nounphrase) leaf nodes of a chunk tree.
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()

def acceptable_word(word):
    #Checks conditions for acceptable word: length, stopword.
    accepted = bool(2 <= len(word) <= 40
        and word.lower() not in stopwords)
    return accepted


def get_terms(tree):
    for leaf in leaves(tree):
        term = [normalise(w) for w, t in leaf if acceptable_word(w) ]
        yield term

"""
chunkGram = r"""#Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""


def make_chunk(text):
    #text = normalise(text)
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    cp = nltk.RegexpParser(chunkGram)

    chunk_parser = nltk.RegexpParser(chunkGram)
    chunged = chunk_parser.parse(pos)
  #  print(chunged)
    array = []
    for subtree in chunged.subtrees(filter=lambda t: t.label() == "#Chunk"):
        array.append(" ".join([a for (a, b) in subtree.leaves()]))

    arr = nltk.FreqDist(array)
    key_chunk = arr.most_common(5)
    return key_chunk

    #return chunged


def normalise(word):
    #Normalises words to lowercase and stems and lemmatizes it.
    word = word.lower()
    word = stemmer.stem(word)
    word = lemmatizer.lemmatize(word)
    return word



def find_ent(text, tag='PERSON'):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary=False)
 #   print(sentt)
    array = []
    for subtree in sentt.subtrees(filter = lambda t: t.label() == tag):
        array.append(" ".join([a for (a, b) in subtree.leaves()]))
    return array

#data = "President Donald Trump, President Putin and President Sauli Niinistö met in Helsinki Finland"
#print(find_ent(data))
#print(make_chunk(data))
#make_chunk(data).draw()