# File contains SQLite DB model for tables

from app import db
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    likes = db.relationship('Like', backref='user', lazy='dynamic')  

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
	date = db.Column(db.Date)
	likes = db.relationship('Like', backref='article', lazy='dynamic')

	# Define how to print article instances
	def __repr__(self):
		return '<Post %r>' % (self.url)

class Like(db.Model):
	__tablename__ = 'like'
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
	like = db.Column(db.Boolean)