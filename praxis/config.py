# praxis/config.py
import os

class Config:
    PRAXIS_ASSISTANT_ID = os.getenv('PRAXIS_ASSISTANT_ID')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False