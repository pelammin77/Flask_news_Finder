"""  
file: main.py 
Author Petri Lamminaho 33

"""

from flask import Flask, request,render_template, url_for
from feedParser import Feed
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





app = Flask(__name__)
COS_SIM = 25.0
feeds_names =[
               'CNN',
                'BBC',
                'NY Times',
                'Washington Post',
                'Fox News',
                'Huffington Post',
                'CNBC'
]

feeds_addresses = [
                'http://rss.cnn.com/rss/edition.rss',
                'http://feeds.bbci.co.uk/news/rss.xml',
                'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
              #  'http://www.goodnewsnetwork.org/feed/',
                'http://feeds.washingtonpost.com/rss/politics',
                'http://feeds.foxnews.com/foxnews/latest',
                'http://www.huffingtonpost.com/feeds/index.xml',
                'http://www.cnbc.com/id/100003114/device/rss/rss.html'
        ]






def get_element_count(url, tag="img"):
    from bs4 import BeautifulSoup
    import requests

    response = requests.get(url)
    soup = BeautifulSoup(response.content)

    return len(soup.find_all(tag))





def get_article_text(link):
    """
    
    :param link: 
    :return: p.get_news_by_link(link) (news title and news text) 
    """
    from Parse import Parser
    p = Parser("")
    return p.get_news_by_link(link)

def remove_extra_text(text):
    text = text.replace(
        'Share this with Copy this link These are external links and will open in a new window', '')
    return text


def readability(text):
    rd = Readability_coountter(text)
    fleasch_ease = rd.flesch_reading_ease()
    fleasch_grade = rd.flesch_kincaid_grade_level()
    readability_text =""
    if fleasch_ease > 90:
        readability_text = "Very easy to read."
    elif 80 < fleasch_ease < 90:
        readability_text = "Easy to read"
    elif 70 < fleasch_ease < 80:
        readability_text = "Fairly easy to read."
    elif 60 < fleasch_ease < 70:
        readability_text = ('PlainEnglish. Easily understood by 13 - to 15 - year - old students.')
    elif 50 < fleasch_ease < 60:
       readability_text = "Fairly difficult to read."
    elif 30 < fleasch_ease < 50:
        readability_text = "Difficult to read."
    elif fleasch_ease > 0 > fleasch_ease:
        readability_text ="Very difficult to read. Best understood by university graduates."
    else:
        readability_text = "Unknown score"

    return fleasch_ease, fleasch_grade, readability_text


def make_summary(text):
    """
    
    :param text: 
    :return: summarizer.summarize(text, 3) (summary array)
    """
    from Summarizer import Summarizer
    from find_ent import make_chunk
    text = remove_extra_text(text)
    summarizer = Summarizer()

    return summarizer.summarize(text, 3), set(make_chunk(text)),\
           summarizer.get_sents_count(), summarizer.get_words_count()

def get_posts_in_one_feed(feed_address):
    feed = Feed(feed_address)
    return feed.get_all_posts()


def get_news(posts):
    for f in feeds_addresses:
        feed = Feed(f)
        arr = feed.get_all_posts()
        posts.append(arr)

    return posts


def clean_article_content(link):
    from cleaner import Html_cleaner
    import urllib.request

    htmlcode = urllib.request.urlopen(link).read().decode('utf-8')
    clean_page = Html_cleaner(htmlcode, link)
    header = clean_page.get_article_title()
    content = clean_page.get_article_content_html()

    return header, content


def find_sim_post_title(title):
    from text_simylarity import is_same_text
    print("News title is:", title)
    posts = []
    sim_post = []
    for f in feeds_addresses:
        feed = Feed(f)
        posts += feed.get_all_posts()

    for p in posts:

        if is_same_text(p.title, title, COS_SIM):
            sim_post.append(p)
            print("find simularity: " + p.title + " " + p.link)

    return sim_post


@app.route('/page')
def page():
     return render_template("about.html")





@app.route('/')
def index():
    news_posts = []
    news_posts = get_news(news_posts)
    print(news_posts[0][0].title)
    return render_template("index.html", feeds_names=feeds_names, news_posts=news_posts)

@app.route('/feed_posts/<int:feed_id>')
def feed_posts(feed_id):
    title = feeds_names[feed_id]
    posts = get_posts_in_one_feed(feeds_addresses[feed_id])
    return render_template('feed_posts.html', title=title, posts=posts)




@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

"""
@app.route('/users/<username>')
def users(username):
    return render_template("profile.html", username=username)
"""


@app.route('/all_news/<feed_id>')
def all_news(feed_id):
    return  render_template("profile.html", feed_id=feed_id) #todo muista muuttaa template


@app.route('/analyze/', methods=['POST'])
def analyze():
    link = request.form['link_field']
    header, text, authors, publish_day, key_words, article_summ, top_image = get_article_text(link)
    summary,  key_chunnks, count_s, count_w = make_summary(text)
    img_count = get_element_count(link)
    video_count = get_element_count(link, 'video')
    #kw = get_KWs(text)
 #   print(kw)
    if publish_day == None:
        publish_day = "unknown"
    fleash_ease_score, fleash_grade, rd_text = readability(text)
    sim_posts = find_sim_post_title(header)
    sim_posts_count = len(sim_posts)
    print(key_words[0])
    return render_template("summary.html", link=link, header=header, summary=summary,
                           article_summ=article_summ, authors=authors, key_words=key_words,
                           publish_day=publish_day, count_s=count_s, top_image=top_image,
                           count_w=count_w, key_chunnks=key_chunnks, sim_posts=sim_posts,
                           img_count=img_count, video_count=video_count,
                           sim_posts_count=sim_posts_count, rd_text=rd_text,
                           fleash_ease_score=fleash_ease_score, fleash_grade=fleash_grade)

@app.route('/clean_article/', methods=['POST'])
def clean_article():
    link = request.form['link_field']
    title, html_content = clean_article_content(link)
    page ="<h1>" + title + "</h1>" + html_content
    return (page)
    #return  render_template("easy_read.html", title=title, html_content=html_content)
    """
    
    
    """




@app.route('/similarity/', methods=['POST'])
def similarity():
    pass

if __name__ == "__main__":
    app.run(debug=True)
