from app import db
import pandas as pd
from scipy.spatial.distance import cosine
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
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
		print(matrix)
		cosine_similarities = linear_kernel(matrix, matrix)
		

		for idx, row in self.articleDF.iterrows():
			""" Iterates through each row in pandas dataframe
			Finds similar items (up to 10) and then sets the 
			'similar_articles' column equal to the list of similar items.
			Stores as str([(similarity score, articleId),...])
			"""
			similar_indices = cosine_similarities[idx].argsort()[:-10:-1]
			similar_items = [(cosine_similarities[idx][i], self.articleDF.id[i]) for i in similar_indices]

			self.articleDF.set_value(idx,'similar_articles',str(similar_items[1:]))
			
		print(self.articleDF)
		self.articleDF.to_csv('test.csv')
		self.articleDF.to_sql('article',config.SQLALCHEMY_DATABASE_URI,if_exists='replace')

if __name__ == '__main__':
	contentEngine = ContentEngine()
	contentEngine.article_based_similarity()