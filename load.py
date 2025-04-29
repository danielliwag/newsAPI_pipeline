from log_config import setup_logger
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from config import DB_CONFIG

logger = setup_logger(__name__)

# Create the database connection engine
def get_engine():
    try:
        db_url = URL.create(
            drivername='postgresql+psycopg2',
            username=DB_CONFIG['user'],
            password=DB_CONFIG['pass'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=DB_CONFIG['name'],
        )
        engine = create_engine(db_url, pool_size=5, max_overflow=10)
        logger.info('PostgreSQL engine created successfully.')
        return engine
    except Exception as e:
        logger.exception(f'Error creating SQLAlchemy engine: {e}')
        raise

# Fetch existing keys from the database for deduplication
def get_existing_keys(table_name, key_column, engine):
    try:
        query = text(f'SELECT {key_column} FROM {table_name}')
        with engine.connect() as conn:
            result = conn.execute(query)
            existing_keys = {row[0] for row in result}
            logger.info(f'Fetched {len(existing_keys)} existing keys from {table_name}')
            return existing_keys
    except Exception as e:
        logger.exception(f'Error fetching existing keys: {e}')
        return set()

# Load data into PostgreSQL database
def load_data_to_postgres(df, table_name, key_column='url', if_exists='append', index=False):
    logger.info(f'Loading data into PostgreSQL table: {table_name}')

    if df.empty:
        logger.warning('No data to load. Skipping insert.')
        return False

    try:
        engine = get_engine()

        # Deduplication based on key_column
        if key_column in df.columns:
            existing_keys = get_existing_keys(table_name, key_column, engine)
            df = df[~df[key_column].isin(existing_keys)]
            logger.info(f'{len(df)} new records after removing duplicates.')
        else:
            logger.warning(f"Key column '{key_column}' not found in DataFrame. Skipping deduplication.")

        if df.empty:
            logger.info('No new data to load after deduplication.')
            return False

        # Use SQLAlchemy engine to load data
        with engine.begin() as connection:
            df.to_sql(
                name=table_name,
                con=connection,
                if_exists=if_exists,
                index=index,
                method='multi',
                chunksize=1000
            )
        logger.info('Data loaded successfully.')
        return True
    except Exception as e:
        logger.exception(f'Failed to load data into {table_name}: {e}')
        return False
