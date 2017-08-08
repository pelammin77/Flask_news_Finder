"""
File: News_article 
Author: Petri Lamminaho
 Made: 15.7.2017  
NewsArticle class contains the data of news article 
"""


class NewsArticle:

    def __init__(self, title, link, text):   # constructor
        self.__title = title
        self.__link = link
        self.__text = text
        self.__summary = []
        self.__keywords = []

# ------------------------------------------------------------#
# get methods                                                 #
# ------------------------------------------------------------#
    def get_title(self):
        return self.__title

    def get_link(self):
        return self.__link

    def get_text(self):
        return self.__text

    def get_summary(self):
        return self.__summary

    def get_keywords(self):
        return self.__keywords

# -----------------------------------------------------------#
# set methods                                                #
# -----------------------------------------------------------#
    def set_title(self, title):
        self.__title = title

    def set_link(self, link):
        self.__link = link

    def set_text(self, text):
        self.__text = text

    def set_summary(self, summary):
        self.__summary = summary

    def set_keywords(self, kws):
        self.__keywords = kws
