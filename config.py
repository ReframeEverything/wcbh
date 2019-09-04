import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get('DATEBASE_URL', 'sqlite:///data.db')
