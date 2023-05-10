import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text

load_dotenv('./.env')

if __name__ == "__main__":
    url_object_one = URL.create(
        "postgresql+psycopg2",
        username=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        port=os.environ['DB_PORT']
    )
    print("Creating database engine...")
    engine_one = create_engine(url_object_one)


    table_names = ["continent","country","plant_cycle","plant","botanist", "sunlight_value", "record", "sunlight_for_plant"]
    for table_name in table_names:
        df = pd.read_sql_table(table_name=table_name,con=engine_one)
        # Download from S3 to tmp here TODO
        try:
            pd.read_csv(f'./tmp/{table_name}.csv')\
                ._append(df).drop_duplicates()\
                    .to_csv(f'./tmp/{table_name}.csv')
        except FileNotFoundError:
            df.to_csv(f'./tmp/{table_name}.csv')
    with engine_one.connect() as con:
        statement = text(
            """
            DELETE FROM record
            """
        )
        con.execute(statement)
        con.commit()
    
    # Now erase records table from the SQL database

