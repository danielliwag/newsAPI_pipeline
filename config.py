from dotenv import load_dotenv
import os

load_dotenv()

API_URL = 'https://newsapi.org/v2/top-headlines'
API_KEY = os.getenv('api_key')

DB_CONFIG = {
    'user':os.getenv('USER'),
    'pass':os.getenv('PASS'),
    'host':os.getenv('HOST'),
    'port':os.getenv('PORT'),
    'name':os.getenv('DB')
}