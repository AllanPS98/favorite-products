import os

class Configurations:

    APP_HOST = os.getenv('APP_HOST', '0.0.0.0')
    APP_PORT = os.getenv('APP_PORT', 8000)
    APP_NAME = os.getenv('APP_NAME', 'Favorite Products')
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    DB_USERNAME = os.getenv('DB_USERNAME', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    DB_NAME = os.getenv('DB_NAME', 'postgres')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_STRING_URI = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    FAKE_STORE_URL = os.getenv('FAKE_STORE_URL', 'https://fakestoreapi.com')
    TIMEZONE = 'America/Sao_Paulo'