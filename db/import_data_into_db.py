from sqlalchemy import create_engine

def import_data_to_db(event_data):

    database="postgres"
    user='postgres'
    password='postgres'
    host='localhost'
    port= '5432'
    

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    conn = engine.connect()

    fact_table_name = 'future_demand_table'
    schema_name = 'future_demand_schema'


    
    event_data.to_sql( fact_table_name, conn, index=False, if_exists='append', schema  = schema_name)
            
   
    conn.commit()

    # Close the connection
    conn.close()

    # Dispose of the engine
    engine.dispose()

    print("i have successfully imported all the Data")


    return(1)