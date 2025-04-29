import requests
from retrying import retry
from config import API_KEY
from log_config import setup_logger

logger = setup_logger(__name__)

@retry(stop_max_attempt_number=3, wait_fixed=3000)
def extract_data(url,params=None):
    logger.info('Data extraction started.')

    if params is None:
        params = {'q':'conclave', 'apiKey': API_KEY}

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        articles = data.get('articles', [])
        logger.info('Data extraction completed successfully.')
        return articles
    
    except requests.exceptions.HTTPError as e:
        logger.exception(f'HTTP error: {e.response.status_code} - {e.response.text}')
    except requests.exceptions.RequestException:
        logger.exception('Network-related error during extraction')
    except ValueError:
        logger.exception('Invalid JSON response')
    except Exception as e:
        logger.exception(f'Unexpected error during data extraction: {e}')

    return None
