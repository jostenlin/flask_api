import datetime

# 配置文件
class Config:
    DEBUG = True
    SECRET_KEY = 'your_secret_key'
    DATABASE_URI = 'your_database_uri'
    
    # flask-jwt-extended 設定
    JWT_SECRET_KEY = 'super-secret'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=30)
    
