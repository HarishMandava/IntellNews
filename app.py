from flask import Flask, redirect, url_for, render_template, flash, request, g, Markup
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
from oauth import OAuthSignIn
import os
import config
import hack
import ast
global titles
import engines

# Initialization of app and database
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app.models import *

app.config['SECRET_KEY'] = 'top secret!'
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id':config.fb_id,
        'secret':config.fb_key
    },
    'twitter': {
        'id': config.twitter_id,
        'secret': config.twitter_key
    }
}

lm = LoginManager(app)
lm.login_view = 'index'


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def index():
    tem=hack.titles

    titles = []
    urls = []
    hacker_ids = []
    ids = []
    keywords = []

    if current_user.is_authenticated:
        hack.processTopArticles()
        articles = g.user.unliked_articles()
        if articles:
	        for article in articles:
	            ids.append(article.id)
	            titles.append(article.title)
	            urls.append(article.url)
	            hacker_ids.append(article.url)
	            keywords.append(article.keywords)

    return render_template('index.html', keywords=keywords, ids=ids,titles=titles,urls=urls,hacker_ids=hacker_ids)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))


@app.route('/like/<articleId>')
def like(articleId):
    article = Article.query.filter_by(id = articleId).first()
    similar_articles = ast.literal_eval(article.similar_articles)

    # Pull any articles that are similar to the one liked
    if int(similar_articles[0][0]) > 0: # article_tuple -> (sim score, articleId)
        similarArticleId = int(similar_articles[0][1])
        similar_article = Article.query.filter_by(id = similarArticleId).first()
        similar_title = similar_article.title
        similar_url = similar_article.url
        similar_keywords = similar_article.keywords
        similar_message = 'Here is another article you might like: <a href=' + similar_url + '>' + similar_title + '</a><br><h6><b>Topcs: </b>' + similar_keywords + '</h6>'
        flash(Markup(similar_message))
    if article is None:
        flash('Article not found')
        return redirect(url_for('index'))
    newLike = g.user.like(article)
    if newLike is None:
        flash('Cannot like article')
        return redirect(url_for('index'))    
    db.session.add(newLike)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/unlike/<articleId>')
def unlike(articleId):
    article = Article.query.filter_by(id = articleId).first()
    if article is None:
        flash('Article not found')
        return redirect(url_for('index'))
    newUnlike = g.user.unlike(article)
    if newUnlike is None:
        flash('Cannot unlike article')
        return redirect(url_for('index'))
    db.session.add(newUnlike)
    db.session.commit()
    flash('You unliked the article')
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
