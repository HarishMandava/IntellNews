# File contains SQLite DB model for tables

from IntellNews import db
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    #preferences = db.relationship('Preference', backref='user', lazy='dynamic')

    # Define how to print users instances
    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Article(db.Model):
	__tablename__ = 'article'
	id = db.Column(db.Integer, primary_key = True)
	hacker_id = db.Column(db.Integer)
	keywords = db.Column(db.String(200))
	url = db.Column(db.String(500))
	#preferences = db.relationship('Preference', backref='article', lazy='dynamic')

	# Define how to print article instances
	def __repr__(self):
		return '<Post %r>' % (self.url)

class Preference(db.Model):
	__tablename__ = 'preference'
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.column(db.Integer, db.ForeignKey('user.id'))
	article_id = db.column(db.Integer, db.ForeignKey('article.id'))
	like = db.Column(db.Boolean)

