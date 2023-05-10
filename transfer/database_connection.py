import os
from psycopg2 import connect, DatabaseError
from psycopg2.extras import RealDictConnection

from dotenv import load_dotenv #remove before dockerising
load_dotenv('./.env') #remove before dockerising


def get_db_connection(config):
    """connects to the required database and raises error if connection fails"""
    try:
        conn = connect(
            user = config["DB_USER"],
            password = config["DB_PASSWORD"],
            host = config["DB_HOST"],
            port = config["DB_PORT"],
            database = config["DB_NAME"],
            connection_factory=RealDictConnection)
        return conn
    except DatabaseError as err:
        print("Error connecting to database: " + err.args[0])


def get_second_db_connection(config):
    """connects to the required database and raises error if connection fails"""
    try:
        conn = connect(
            user = config["DB_USER_2"],
            password = config["DB_PASSWORD_2"],
            host = config["DB_HOST_2"],
            port = config["DB_PORT_2"],
            database = config["DB_NAME_2"],
            connection_factory=RealDictConnection)
        return conn
    except DatabaseError as err:
        print("Error connecting to database: " + err.args[0])