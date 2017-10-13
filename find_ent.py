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


def remove_stopwords(text):
    from nltk.corpus import stopwords
    from string import punctuation
    from nltk.tokenize import sent_tokenize, word_tokenize
    filt_text = []
    stopwords = set(stopwords.words('english') + list(punctuation))
    stopwords.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
    words = word_tokenize(text)
    for w in words:
        if w not in stopwords:
            filt_text.append(w)
    filter_str = ''.join(filt_text)
    return filter_str





def make_chunk(text):
    from nltk.corpus import stopwords
    from string import punctuation
    stopwords = set(stopwords.words('english') + list(punctuation))
    stopwords.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '”', '“', "Advertisement"])

    print(text)
    f_tokens = []
    #text = remove_stopwords(text)
    #text = normalise(text)
    tokens = nltk.tokenize.word_tokenize(text)
    for w in tokens:
        if w not in stopwords:
            f_tokens.append(w)

    pos = nltk.pos_tag(f_tokens)
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

def find_all_ent(sentt, tag ):
    array = []
    for subtree in sentt.subtrees(filter = lambda t: t.label() == tag):
        array.append(" ".join([a for (a, b) in subtree.leaves()]))
    #print(array)
    return  array

def find_ent(text):
    all_ents = []
    arr = []
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary=False)
  #  all_ents = all_ents.extend(find_all_ent(sentt, 'ORGANIZATION'))
    all_ents += find_all_ent(sentt, 'PERSON')
    all_ents += find_all_ent(sentt, 'LOCATION')
    all_ents += find_all_ent(sentt, 'DATE')
   # all_ents += find_all_ent(sentt, 'TIME')
  #  all_ents += find_all_ent(sentt, 'MONEY')
    all_ents += find_all_ent(sentt, 'FACILITY')
    all_ents += find_all_ent(sentt, 'GPE')

    return set(all_ents)

data = "President Donald Trump, President Putin and President Sauli Niinistö met in Helsinki Finland"
data2 = "Media playback is unsupported on your device Media caption Dame Louise Casey compares the government's " \
        "Universal Credit welfare plan to jumping over a cliff Families could be left homeless and destitute if Theresa " \
        "May insists on pressing ahead with Universal Credit, a former top adviser has warned. Official figures show " \
        "about one in four new Universal Credit claimants wait longer than six weeks to be paid - causing many to fall " \
        "behind on rent. He says he and his girlfriend were evicted from their shared flat about six months ago once " \
        "their landlord found out they were on Universal Credit. Basically because we were on Universal Credit and he's " \
        "had a lot of people not paying the rent... we got kicked out." "As soon as I go to meet them and say I am on " \
        "Universal Credit, it's a no: 'We ain't got no rooms.'"

data3 ="And health care is sure to be an issue in next year’s midterm elections. Senator John Thune of South Dakota, a member of the Senate Republican leadership, said the concept behind the Graham-Cassidy bill would help Republicans define their differences with Democrats in the campaign season. Senate Republicans tried in July to approve a repeal bill, but that attempt ended in defeat when Senator John McCain, Republican of Arizona, gave a thumbs-down, killing that version of the legislation. Advertisement Continue reading the main storyAfter tackling the tax overhaul, Republicans could make another attempt at passing a health bill without needing any Democratic votes. Even as Republicans shift their focus to taxes, pressure is building for a bipartisan response to the problems of the health care system. "

print(find_ent(data3))
#print(make_chunk(data))
#make_chunk(data).draw()