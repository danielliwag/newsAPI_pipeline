import pandas as pd
from log_config import setup_logger

logger = setup_logger(__name__)

def transform_data(raw_data):
    logger.info('Data transformation started.')
    
    if not raw_data:
        logger.warning('No data to transform.')
        return pd.DataFrame()
    
    try:
        df = pd.json_normalize(raw_data)
        
        cols_to_strip = ['author', 'title', 'description', 'content', 'source.id', 'source.name']
        for col in cols_to_strip:
            df[col] = df[col].str.strip()

        df.columns = df.columns.str.lower()

        df['source.id'] = df['source.name'].str.replace(' ', '-').str.lower()

        df['publishedat'] = pd.to_datetime(df['publishedat'], errors='coerce')

        df = df.rename(columns={'source.id':'source_id', 'source.name':'source_name'})

        logger.info('Data transformation finished successfully.')
        return df
    except (ValueError, TypeError) as e:
        logger.exception(f'Data type issue during transformation: {e}')
    except Exception as e:
        logger.exception(f'Problem has occured during transformation: {e}')

    return pd.DataFrame()