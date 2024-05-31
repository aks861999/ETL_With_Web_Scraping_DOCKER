from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from web_scrap import scarper_extract


import logging

# Configure the logger
logging.basicConfig(
    level=logging.INFO,  # Set the default log level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log message format
)

LOGGER = logging.getLogger(__name__)


database="postgres"
user='postgres'
password='postgres'
host='localhost'
port= '5432'


#engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
#conn = engine.connect()



engine = create_engine('postgresql://{}:{}@{}/{}'.format('postgres','postgres','postgres:5432','future_db'))


# retry mechanism

while(True):
    try:
        db_engine = engine.connect()
        if db_engine:
            break
    except Exception as e:
        print(e)
        LOGGER.warning(e)

# URL of the Lucerne Festival 2024 Summer program
url = "https://www.lucernefestival.ch/en/program/summer-festival-24"

event_data = scarper_extract(url)



# here conn == db_engine

fact_table_name = 'future_table'
schema_name = 'future_schema'


try:
    with db_engine as conn:
        event_data.to_sql( fact_table_name, conn, index=False, if_exists='append', schema  = schema_name)
    LOGGER.info("Successfully imported all the data")

except SQLAlchemyError as e:
    LOGGER.warning("An error occurred:", e)

finally:

    # Dispose of the engine
    engine.dispose()