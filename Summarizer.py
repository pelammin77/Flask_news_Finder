from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
from nltk.corpus import wordnet
from collections import defaultdict
from string import punctuation
from heapq import nlargest



class Summarizer:
    def __init__(self, min_sum=0.1, max_sum=0.9):
        self._min_sum = min_sum
        self._max_sum = max_sum
        self._stopwords = set(stopwords.words('english') + list(punctuation))
        #self._stopwords.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{','}'])
        self._stopwords.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '”', '“', "Advertisement"])

    def _compute_words(self, words_sen):
        freq = defaultdict(int)

        for sen in words_sen:
            for word in sen:
                if word not in self._stopwords:
                    freq[word] += 1
        m = float(max(freq.values()))
        for w in freq.copy().keys():
            freq[w] = freq[w] / m
            if freq[w] >= self._max_sum or freq[w] <= self._min_sum:
                del freq[w]
        return freq

    def getSentsLen(self, text):
        sen = sent_tokenize(text)
        return len(sen)

    def summarize(self, text, n):
        text = text.strip()
        sents = sent_tokenize(text)
        words = word_tokenize(text)
        if len(sents)< 2:
            return ''

        assert n <= len(sents)
        self.count_of_sens = len(sents)
        #self.first_sen = sents[0]
        self.count_of_words = len(words)
        word_sent = [word_tokenize(s.lower()) for s in sents]
        self._freq = self._compute_words(word_sent)
        ranking = defaultdict(int)
        for i, sent in enumerate(word_sent):
            for w in sent:
                if w in self._freq:
                    ranking[i] += self._freq[w]
        sents_idx = self._rank(ranking, n)
        return [sents[j] for j in sents_idx]

    def _rank(self, ranking, n):
        r = nlargest(n, ranking, key=ranking.get)
        # print(r)
        return r

    def get_sents_count(self):
        return self.count_of_sens

    def get_words_count(self):
        return self.count_of_words


    def get_key_words(self, text, words_count=5):





       '''' words = word_tokenize(text)
        words = nltk.FreqDist(words)
        print(words.most_common(words_count))
'''