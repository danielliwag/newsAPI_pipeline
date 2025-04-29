from dotenv import load_dotenv
import os

load_dotenv()

API_URL = 'https://newsapi.org/v2/everything'
API_KEY = os.getenv('api_key')