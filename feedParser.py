from Summarizer import Summarizer
from Parse import Parser
#from find_ent import find_ent
from find_ent import make_chunk
#import text_senti as senti
"""
# Feeds
# ----------------------------------------------------------------------------
CNN = 'http://rss.cnn.com/rss/edition.rss'
BBC = 'http://feeds.bbci.co.uk/news/rss.xml'
NY_TIMES = 'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'
GOOD_NEWS = 'http://www.goodnewsnetwork.org/feed/'
WSHG_POST = 'http://feeds.washingtonpost.com/rss/politics'
FOX_NEWS = 'http://feeds.foxnews.com/foxnews/latest'
HUFF_POST = 'http://www.huffingtonpost.com/feeds/index.xml'
CNBC = 'http://www.cnbc.com/id/100003114/device/rss/rss.html'

# ---------------------------------------------------------------------------
"""


class Feed:
    def __init__(self, feed_url):

        self.__feed_url = feed_url
        self.__parser = Parser(feed_url)

        #self.__title = ""
        #self.__text
        self.__summary = Summarizer()
        self.__key_phasers =[]




    def get_all_posts(self):
        return self.__parser.get_all_news_links_from_feed()

    def get_article(self, post_i):
        self.__title, self.__text = self.__parser.get_news(post_i)


    def make_summary(self, n=3):
        self.__text = self.__text.replace('Share this with Copy this link These are external links and will open in a new window', '')
        #print("\nArticle title:", self.__title + "\n")
        #print('Key words:', set(find_ent(self.__text)))

        #print('Article summary:')
        #for s in self.__summary._summarize(self.__text, n ):
         #   print('*', s)
        #print(senti.sentiment(self.__text))


    def find_key_chunks(self):
        self.__key_phasers = set(make_chunk(self.__text))
        return self.__key_phasers

    def get_title(self):
        return self.__title


"""
def find_feeds(feed_url):
    parser = Parser(feed_url)
    parser.get_news()
"""
