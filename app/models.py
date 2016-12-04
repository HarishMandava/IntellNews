# File contains SQLite DB model for tables

from app import db
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user


likes = db.Table('likes', # Not a full class because only storing relational information
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    liked = db.relationship('Article',
                            secondary=likes,
                            #primaryjoin=(likes.c.user_id == id),
                            #secondaryjoin=(likes.c.article_id == id),
                            backref=db.backref('liked_by', lazy='dynamic'),
                            lazy='dynamic')


    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def like(self, article):
        """ Returns an object when succeeds """
        if not self.has_liked(article):
            self.liked.append(article)
            return self
    
    def unlike(self, article):
        """ Returns an object when succeeds """
        if self.has_liked(article):
            self.liked.remove(article)
            return self

    def has_liked(self, article):
        """ Taking liked relationship query which returns (user_id, article_id) pairs
        where the user liked an article, and filter by the article.  The filter() call
        returns query without it being executed. Then we call count on this query,
        which causes the query to execute and return the number of records found.  If
        returns greater than 0, we know user liked that article. If we get none,
        then user has not yet liked the article.
        """
        return self.liked.filter(likes.c.article_id == article.id).count() > 0

    def liked_articles(self):
        """ Queries Likes table to get temp table of articles that have likes.
        Then filters that table for any that have been liked by current user.
        Then sorts that table by the date the article was retrieved from HN,
        i.e., the newest articles.
        """
        return Article.query.join(likes, 
            (likes.c.article_id == Article.id)).filter(likes.c.user_id == self.id).order_by(Article.date.desc())

    def unliked_articles(self):
    	""" Returns articles that a user has not liked
    	"""
    	return Article.query.outerjoin(likes,
    		(likes.c.article_id == Article.id)).filter((likes.c.user_id == None) | (likes.c.user_id != self.id))

    # Define how to print users instances
    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key = True)
    hacker_id = db.Column(db.Integer)
    title = db.Column(db.String(200))
    url = db.Column(db.String(500))
    keywords = db.Column(db.String(2000))
    date = db.Column(db.Date) # Date retrieved from Hacker News by app

    # Define how to print article instances
    def __repr__(self):
        return '<Article Title: %r>' % (self.title)


