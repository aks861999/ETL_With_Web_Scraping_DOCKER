
import psycopg2
from psycopg2 import sql

def create_table(cursor, table_name):
    try:
        # Create the table with fixed columns and extra columns
        columns = [
            "Event_Title TEXT",
            "Artist TEXT",
            "Day TEXT",
            "date_string TEXT",
            "Time TEXT",
            "Location TEXT",
            "works TEXT",
            "image_link TEXT"
        ]
        create_table_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS future_demand_schema.{table_name} (
                {columns}
            );
        """).format(
            table_name=sql.Identifier(table_name),
            columns=sql.SQL(', ').join(map(sql.SQL, columns))
        )

        cursor.execute(create_table_query)
        
        cursor.connection.commit()
        print(f"Table '{table_name}' created successfully.")

    except psycopg2.Error as e:
        print(f"Error: {e}")




def schema_table_creation():
    database="postgres"
    user='postgres'
    password='postgres'
    host='localhost'
    port= '5432'

    # Creating tables with different numbers of extra columns
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(user=user, password=password, host=host, port=port, database = database)
        cursor = conn.cursor()

        cursor.execute("CREATE SCHEMA IF NOT EXISTS future_demand_schema;")

        # create_table(cursor, <table_name>)
        create_table(cursor,"future_demand_table")  

    except psycopg2.Error as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()


    return(1)