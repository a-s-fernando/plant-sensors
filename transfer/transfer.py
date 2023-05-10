import os
import pandas as pd
from sqlalchemy import create_engine, URL, text
import s3fs


def handler(event, context):
    """lambda handler function to move data from rds to csv and store in s3"""
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


    table_names = ["continent","country","plant_cycle","plant","botanist",
                   "sunlight_value", "record", "sunlight_for_plant"]
    s3 = s3fs.S3FileSystem(anon=False, key=os.environ['ACCESS_KEY'], secret=os.environ['SECRET_KEY'])

    for table_name in table_names:
        df = pd.read_sql_table(table_name=table_name,con=engine_one)
        print("Accessing S3...")
        try:
            with s3.open(f"c7-aaa-s3-bucket/{table_name}.csv", mode='r') as s3_file, open(f"/tmp/{table_name}.csv", mode='w') as file:
                file.write(s3_file.read())
            pd.read_csv(f'/tmp/{table_name}.csv')\
                ._append(df).drop_duplicates()\
                    .to_csv(f'/tmp/{table_name}.csv')
            with s3.open(f"c7-aaa-s3-bucket/{table_name}.csv", mode='w') as s3_file, open(f"/tmp/{table_name}.csv", mode='r') as file:
                s3_file.write(file.read())
                print("Appended to csv.")

        except Exception:
            df.to_csv(f'/tmp/{table_name}.csv')
            with s3.open(f"c7-aaa-s3-bucket/{table_name}.csv", mode='w') as s3_file, open(f"/tmp/{table_name}.csv", mode='r') as file:
                s3_file.write(file.read())
                print("Created csv.")

    with engine_one.connect() as con:
        statement = text("DELETE FROM record")
        con.execute(statement)
        con.commit()
        print("Deleted records.")

if __name__ == "__main__":
    handler(None, None)
