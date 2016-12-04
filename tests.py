""" Test Cases """
import os
import unittest
from datetime import datetime, timedelta

from config import basedir
from app import app, db
from app.models import User, Article, likes

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'test.db')
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_like(self):
        """ Tests the like feature """

        # Create user and article
        u1 = User(social_id = '123', nickname='john', email='john@doe.com')
        a1 = Article(hacker_id = 10239840, title='The Most Interesting Article Ever', url='http://test.com', keywords='[interesting]')
        a2 = Article(hacker_id = 23982350, title='Another Tech Article', url='http://test.com', keywords='[tech]')
        db.session.add(u1)
        db.session.add(a1)
        db.session.add(a2)
        db.session.commit()
        
        # Make sure that user does not like article already
        assert u1.unlike(a1) is None    # Returns none if user can't unlike
        unlikedArticles = u1.unliked_articles().all()

        
        # User likes the first article
        ulike1 = u1.like(a1)
        db.session.add(ulike1)
        db.session.commit()
        unlikedArticles = u1.unliked_articles().all()
        assert len(unlikedArticles) == 1
        assert unlikedArticles == [a2]

        # User likes the second article
        ulike2 = u1.like(a2)
        db.session.add(ulike2)
        db.session.commit()
        unlikedArticles = u1.unliked_articles().all()
        assert len(unlikedArticles) == 0
        assert unlikedArticles == []

        # Check that user cannot re-like the article (already liked it)
        assert u1.like(a1) is None
        assert u1.has_liked(a1)
        assert u1.like(a2) is None
        assert u1.has_liked(a2)
        assert u1.liked.count() == 2
        assert u1.liked.first().hacker_id == 10239840
        likedArticles = u1.liked_articles().all()
        assert len(likedArticles) == 2
        assert likedArticles == [a1, a2]
        assert a1.liked_by.count() == 1
        assert a1.liked_by.first().nickname == 'john'
        
        # Check user can unlike the article
        ulike1 = u1.unlike(a1)
        ulike2 = u1.unlike(a2)
        assert ulike1 is not None
        assert ulike2 is not None
        db.session.add(ulike1)
        db.session.add(ulike2)
        db.session.commit()
        assert not u1.has_liked(a1)
        assert u1.liked.count() == 0
        assert a1.liked_by.count() == 0

if __name__ == '__main__':
    unittest.main()