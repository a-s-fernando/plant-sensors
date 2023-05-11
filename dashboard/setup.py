import os
import pandas as pd
import plotly.express as px
import s3fs
from dotenv import load_dotenv


def get_credentials():
    '''Retrive AWS credentials from local environment'''
    try:
        load_dotenv()
        config = os.environ
        return config
    except Exception as err:
        print("Error loading environment variables", err)

    return config

def get_bucket_connection():
    '''Connects to a given AWS S3 bucket.'''
    config = get_credentials()
    bucket = s3fs.S3FileSystem(anon=False, key=config.get('ACCESS_KEY_ID'), secret=config.get('SECRET_ACCESS_KEY'))

    return bucket

def get_file_from_s3(bucket_name: str) -> str:
    '''Check if input bucket has new XML files'''
    bucket = get_bucket_connection()
    finder = bucket.find(bucket_name)
    for file in finder:
        bucket.get(file, f'./data/{file}')




if __name__ == "__main__":

    get_file_from_s3("c7-aaa-s3-bucket")