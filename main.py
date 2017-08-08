from flask import Flask, request,render_template, url_for
from feedParser import Feed
from text_tb import get_KWs
from News_article import NewsArticle
from News_article import NewsArticle
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

def get_post(post_id):
    pass


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




def get_news(posts):
    for f in feeds_addresses:
        feed = Feed(f)
        arr = feed.get_all_posts()
        posts.append(arr)

    return posts



def find_sim_post_title(title):
    from text_simylarity import is_same_text
    print("News title is:", title)
    posts = []
    sim_post = []
    for f in feeds_addresses:
        feed = Feed(f)
        posts = feed.get_all_posts()

    for p in posts:

        if is_same_text(p.title, title, COS_SIM):
            sim_post.append(p)
            print("find simularity: " + p.title + " " + p.link)

    return sim_post


@app.route('/')
def index():
    news_posts = []
    news_posts = get_news(news_posts)
    print(news_posts[0][0].title)
    return render_template("index.html", feeds_names=feeds_names, news_posts=news_posts)


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
    header, text, authors, publish_day, key_words = get_article_text(link)
    summary,  key_chunnks, count_s, count_w = make_summary(text)
    kw = get_KWs(text)
    print(kw)
    if publish_day == None:
        publish_day = "unknown"

    sim_posts = find_sim_post_title(header)
    return render_template("summary.html", link=link, header=header, summary=summary,
                           authors=authors, publish_day=publish_day, count_s=count_s,
                           count_w=count_w, key_chunnks=key_chunnks, sim_posts=sim_posts)

@app.route('/similarity/', methods=['POST'])
def similarity():
    title = request.form['title_field']
    sim_arr = find_sim_post_title(title)
    print(len(sim_arr))
    return ('<h1> Simularity </h1>')

if __name__ == "__main__":
    app.run(debug=True)
