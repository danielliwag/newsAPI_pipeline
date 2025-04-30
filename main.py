from extract import extract_data
from transform import transform_data
from load import load_data_to_postgres
from log_config import setup_logger
from config import API_URL

logger = setup_logger(__name__)

def run_etl():
    logger.info('Pipeline started running.')
    try:
        raw_data = extract_data(API_URL)
        cleaned_data = transform_data(raw_data)
        load_data_to_postgres(cleaned_data, 'newsapi', key_column='source_id', if_exists='append', index=False)
    except Exception as e:
        logger.exception(f'Problem occured while running pipeline: {e}')

if __name__ == '__main__':
    run_etl()