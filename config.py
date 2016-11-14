import os

# Grabs folder where script runs
basedir = os.path.abspath(os.path.dirname(__file__))

# True for error and debug information
DEBUG = False

#ADMINS = frozenset(['joshgarlitos@gmail.com'])
#SECRET_KEY = 'This string will be replaced with a proper key in production.'

# Database Config for Flask-SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') # DB path
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository') # Storage for migration files
DATABASE_CONNECT_OPTIONS = {}

#THREADS_PER_PAGE = 8

# Web Form Protection Against Post-Fraud
# WTF_CSRF_ENABLED = True
# WTF_CSRF_SECRET_KEY = ""