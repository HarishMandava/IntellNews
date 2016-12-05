from app import db
import pandas as pd
from scipy.spatial.distance import cosine
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sqlalchemy import update
from app.models import *
import os
import config

basedir = os.path.abspath(os.path.dirname(__file__))

class ContentEngine(object):

	# Read in users table
	def __init__(self):
		self.userDF = pd.read_sql_table('user', config.SQLALCHEMY_DATABASE_URI)
		self.articleDF = pd.read_sql_table('article', config.SQLALCHEMY_DATABASE_URI)
		self.likesDF = pd.read_sql_table('likes', config.SQLALCHEMY_DATABASE_URI)

	def article_based_similarity(self):

		vector = CountVectorizer()
		matrix = vector.fit_transform(self.articleDF.keywords)
		cosine_similarities = linear_kernel(matrix, matrix)
		

		for idx, row in self.articleDF.iterrows():
			""" Iterates through each row in pandas dataframe
			Finds similar items (up to 10) and then sets the 
			'similar_articles' column equal to the list of similar items.
			Stores as str([(similarity score, articleId),...])
			"""
			similar_indices = cosine_similarities[idx].argsort()[:-4:-1] # Change -2 to -n for n number of similar articles to be stored
			similar_items = [(cosine_similarities[idx][i], self.articleDF.id[i]) for i in similar_indices]
			similar_items = str(similar_items[1:]) # [1:] beacuse the first item is always same article as self

			article = Article.query.filter(Article.id == row.id).first()
			article.similar_articles = similar_items
			db.session.commit()


if __name__ == '__main__':
	contentEngine = ContentEngine()
	contentEngine.article_based_similarity()