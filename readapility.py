import math
from utils import get_char_count, get_sentences, get_words
from utils import count_complex_words, count_syllables

class Readability_coountter:
    ana_vars = {}

    def __init__(self, text):
        self.analyze_text(text)



    def analyze_text(self, text):
        words = get_words(text)
        char_count = get_char_count(words)
        words_count = len(words)
        sentence_count = len(get_sentences(text))
        syllable_count = count_syllables(words)
        print("syllable_count:", syllable_count)
        complex_words_count = count_complex_words(text)
        avg_words_per_sentence =int(words_count/sentence_count)
        print("avg_words_per_sentence", avg_words_per_sentence)
        self.ana_vars = {
            'words': words,
            'char_count' : float(char_count),
            'words_count' : float(words_count),
            'sentence_count': float(sentence_count),
            'syllable_count': float(syllable_count),
            'complex_words_count': float(complex_words_count),
            'avg_words_per_sentence': float(avg_words_per_sentence)
        }
    def ARI(self):
        score = 0.0
        if self.ana_vars['words_count'] > 0.0:
            score = 4.71 * (self.ana_vars['char_count'] / self.ana_vars['words_count']) + 0.5 *(self.ana_vars['words_count'] / self.ana_vars['sentence_count']) - 21.43
        return round(score, 2)

    def flesch_reading_ease(self):
        score = 0.0
        if self.ana_vars['words_count'] > 0.0:
            score = 206.835 - (1.015 * (self.ana_vars['avg_words_per_sentence'])) - (84.6 * (self.ana_vars['syllable_count']/ self.ana_vars['words_count']))
        return round(score, 4)

    def flesch_kincaid_grade_level(self):
        score = 0.0
        if self.ana_vars['words_count'] > 0.0:
            #print("Syliable float:", self.ana_vars['syllable_count'])
            score = 0.39 * (self.ana_vars['avg_words_per_sentence']) + 11.8 * (self.ana_vars['syllable_count'] / self.ana_vars['words_count']) - 15.59
        return round(score, 4)



    def gunning_fog_index(self):
        score = 0.0
        if self.ana_vars['words_count'] > 0.0:
            score = 0.4 * ((self.ana_vars['avg_words_per_sentence']) + (100 * (self.ana_vars['complex_words_count'] / self.ana_vars['words_count'])))
        return round(score, 4)



    def SMOGIndex(self):
        score = 0.0
        if self.ana_vars['words_count'] > 0.0:
            score = (math.sqrt(self.ana_vars['complex_words_count'] * (30 / self.ana_vars['sentence_count'])) + 3)
        return score



    def coleman_liau_index(self):
        score = 0.0
        if self.ana_vars['words_count'] > 0.0:
            score = (5.89 * (self.ana_vars['char_count'] / self.ana_vars['words_count'])) - (30 * (self.ana_vars['sentence_count'] / self.ana_vars['words_count'])) - 15.8
        return round(score, 4)

    def LIX(self):
        long_words = 0.0
        score = 0.0
        if self.ana_vars['words_count'] > 0.0:
            for word in self.ana_vars['words']:
                if len(word) >= 7:
                    long_words += 1.0
            score = self.ana_vars['words_count'] / self.ana_vars['sentence_count'] + float(100 * long_words) / self.ana_vars['words_count']
        return score


    def RIX(self):
        longwords = 0.0
        score = 0.0
        if self.ana_vars['words_count'] > 0.0:
            for word in self.ana_vars['words']:
                if len(word) >= 7:
                    longwords += 1.0
            score = longwords / self.ana_vars['sentence_count']
        return score



if __name__ == "__main__":
    text = """We are close to wrapping up our 10 week Rails Course. This week we will cover a handful of topics commonly encountered in Rails projects. We then wrap up with part 2 of our Reddit on Rails exercise!  By now you should be hard at work on your personal projects. The students in the course just presented in front of the class with some live demos and a brief intro to to the problems their app were solving. Maybe set aside some time this week to show someone your progress, block off 5 minutes and describe what goal you are working towards, the current state of the project (is it almost done, just getting started, needs UI, etc.), and then show them a quick demo of the app. Explain what type of feedback you are looking for (conceptual, design, usability, etc.) and see what they have to say.  As we are wrapping up the course you need to be focused on learning as much as you can, but also making sure you have the tools to succeed after the class is over."""
   # text = """My name is Pete"""
    rd = Readability_coountter(text)
    print("TEST:")
    print('"%s"\n' % text)
    print("ARI:",  rd.ARI())
    print("FleaschReadingEase:", rd.flesch_reading_ease())
    print("FleschKincaidGradeLevel:", rd.flesch_kincaid_grade_level())
    print("GunningFogIndex:", rd.gunning_fog_index())
    print("Smog_Index:", rd.SMOGIndex())
    print("Coleman index:", rd.coleman_liau_index())
    print("LIX:", rd.LIX())
    print("RIX:", rd.RIX())
