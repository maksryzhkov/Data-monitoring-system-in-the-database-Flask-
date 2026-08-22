import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-for-dev'
    # Указываем точный путь к нашей тестовой базе в папке instance
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'test_data.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False