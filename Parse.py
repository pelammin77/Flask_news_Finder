import feedparser
import bs4 as bs
from newspaper import Article
import text_simylarity


class Parser:
    def __init__(self):
        self.__link = ""
        self._text = ""
        self._title = ""
        self._summary = ""

    def __init__(self, link):

        self.__link = link
        self._text = ""
        self._title = ""
        self._authors = []
        self.__feeds = feedparser.parse(self.__link)

    def find_sim_titles(self, t):
        print("Title:", t)
        for post in self.__feeds.entries:
            print(post.title)
            res = self.compare_texts_sim(post.title, t)

            if res == True:
              print(post.link)

    def get_all_news_links_from_feed(self):
        posts_arr = self.__feeds.entries
        return posts_arr
       # for post in self.__feeds.entries:
            #print(post.title+":"+post.link)
        #    posts_arr.append(post)


           # print(post.title + ":" + post.link)

    def __parse_feed(self, i=0):
        news = self.__feeds.entries[i]
        print(news.link)
       # parseArticle(news.link)
        try:
            article = Article(news.link)
            article.download()
            article.parse()
            article.nlp()
            self._sauce = article.html
            self._authors = article.authors
            self._title = article.title
            self._summary = article.summary
            self._publish_date = article.publish_date
            self._key_words = article.keywords
            self._text = article.text
            self._top_image = article.top_image
            self.__make_soup()

        except:
            print("cannot find web page")
            exit(440)

    def __make_soup(self): # private

        self.__soup = bs.BeautifulSoup(self._sauce, 'html.parser')
        self.__parse_news()

    def __parse_news(self): # private
        import urllib.request
        from cleaner import Html_cleaner
        #print("URL:", self.__link)
        #htmlcode = urllib.request.urlopen(self.__link).read().decode('utf-8')
        #clean_page = Html_cleaner(htmlcode, self.__link)

        [s.extract() for s in self.__soup('style')]
        [s.extract() for s in self.__soup('a')]
        [s.extract() for s in self.__soup('span')]
        self._title = self.__soup.find('title').text
    #    self._text = clean_page.get_article_content_text()
        self._text = ' '.join(map(lambda p: p.text, self.__soup.find_all('p')))

    def get_news_by_link(self, link):
        article = Article(link)
        article.download()
        article.parse()
        article.nlp()
        self._sauce = article.html
        self._authors = article.authors
        self._title = article.title
        self._key_words = article.keywords
        self._publish_date = article.publish_date
        self._summary = article.summary
        self._text = article.text
        self._top_image = article.top_image

        self.__make_soup()
        return self._title, self._text, self._authors, self._publish_date, \
               self._key_words, self._summary, self._top_image


    def get_news(self, i=0):
        self.__parse_feed(i)
        return self._title, self._text

    def compare_texts_sim(self, t1, t2):
        print("vertailaan", t1, "ja", t2)
        res = text_simylarity.compare_texts(t1, t2)

        print("Text simularity is %", res * 100)
        if res>0.15:
            return True