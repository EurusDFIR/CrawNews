import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:eurus@localhost:5432/crawNews'
    SQLALCHEMY_TRACK_MODIFICATIONS = False