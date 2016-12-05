""" Setting up the HackerNews API and analyzing keywords
of the articles from HackerNews
"""

from hackernews import HackerNews
import newspaper
import datetime
from app import db
from app.models import *
import engines


global titles
titles=list()
urls=list()
x=HackerNews()
"""i=0
for id in x.top_stories(limit=6):
    titles.append(x.get_item(id).title)
    urls.append(x.get_item(id).url)
    i += 1
"""

def processTopArticles(limit = 5):
    """ Grab top 6 articles and analyze their content
    """
    articleInsertList = []
    today = datetime.datetime.utcnow() # Grab current date for storing in DB

    for id in x.top_stories(limit):    # Limit is # of stories
        hacker_id = id
        title = x.get_item(id).title
        url = x.get_item(id).url

        # Use Newspaper to analyze keywords
        article = Article.query.filter_by(hacker_id = hacker_id).first()
        if article is None and url is not None:
            article = newspaper.Article(url)
            article.download() # Must download before parse
            if article.html:
                article.parse()
                if article.text: # Must parse before nlp
                    article.nlp() # Must nlp to get keywords
                    if article.keywords:
                        hacker_id = id
                        title = x.get_item(id).title
                        url = x.get_item(id).url
                        keywords = str(article.keywords)
                        
                        # Check if we already have that article stored
                        article = Article.query.filter_by(hacker_id=hacker_id).first()
                        if not article: # if not already stored, then store it
                            article = Article(hacker_id=hacker_id, title=title, 
                                url=url, keywords=keywords, date=today, similar_articles='')
                            db.session.add(article)
                            db.session.commit()

    contentEngine = engines.ContentEngine()
    contentEngine.article_based_similarity()

    return articleInsertList

