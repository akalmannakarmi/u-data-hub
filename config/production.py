from .default import Config

class ProductionConfig(Config):
    SECRET_KEY = 'your_production_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/db_name'
