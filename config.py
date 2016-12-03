import os
basedir = os.path.abspath(os.path.dirname(__file__))

fb_id="550237518504458"
fb_key="1953cfc77cc31b32679eae4fb7974a60"
twitter_id = 'fu8EtaibKfPcyGqxCp6x0RhEm'
twitter_key = 'unpjE6PTGz5GNDpK5chU0OTotqEiOkPMwTY9q6pOv9cAMR5vrR'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')