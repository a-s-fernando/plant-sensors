import os
from time import perf_counter

from extract import get_dataframe, clean_dataframe
from database_connection import get_db_connection

from dotenv import load_dotenv #remove before dockerising
import pandas as pd

# Go through row by row of df using iter rows

# Fill sub-tables

# Check if exists, if not insert, else get id

def load_continents(record, cur) -> int:
    continent = record['origin_continent']
    cur.execute("SELECT * FROM continent WHERE name = %s", (continent,))
    result = cur.fetchone()
    if result:
        id = result['continent_id']
    else:
        cur.execute('INSERT INTO continent (name) VALUES (%s) RETURNING continent_id',
                    (continent,))
        id = cur.fetchone()['continent_id']
    return id


def load_countries(continent_id, record, cur) -> int:
    country = record['origin_country']
    cur.execute("SELECT * FROM country WHERE name = %s", (country,))
    result = cur.fetchone()
    if result:
        id = result['country_id']
    else:
        cur.execute('INSERT INTO country (name, continent_id) VALUES (%s, %s) RETURNING country_id',
                    (country, continent_id,))
        id = cur.fetchone()['country_id']
    return id


def load_plant_cycles(record, cur) -> int:
    plant_cycle = record['plant_cycle']
    cur.execute("SELECT * FROM plant_cycle WHERE value = %s", (plant_cycle,))
    result = cur.fetchone()
    if result:
        id = result['plant_cycle_id']
    else:
        cur.execute('INSERT INTO plant_cycle (value) VALUES (%s) RETURNING plant_cycle_id',
                    (plant_cycle,))
        id = cur.fetchone()['plant_cycle_id']
    return id


def load_plants(record, cur, plant_cycle_id, country_id) -> int:
    name = record['name']
    cur.execute("SELECT * FROM plant WHERE name = %s", (name,))
    result = cur.fetchone()
    if result:
        id = result['plant_id']
    else:
        cur.execute('INSERT INTO plant (name, country_id, plant_cycle_id) VALUES (%s, %s, %s) RETURNING plant_id',
                    (name, country_id, plant_cycle_id,))
        id = cur.fetchone()['plant_id']
    return id


def load_botanist(record, cur) -> int:
    first_name = record['first_name']
    last_name = record['last_name']
    email = record['email']
    cur.execute("SELECT * FROM botanist WHERE first_name = %s AND last_name = %s",
                (first_name, last_name,))
    result = cur.fetchone()
    if result:
        id = result['botanist_id']
    else:
        cur.execute('INSERT INTO botanist (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING botanist_id',
                    (first_name, last_name, email,))
        id = cur.fetchone()['botanist_id']
    return id


def load_sunlight_value(value, cur) -> int:
    value = str(value).lower().strip()
    cur.execute("SELECT * FROM sunlight_value WHERE value = %s", (value,))
    result = cur.fetchone()
    if result:
        id = result['sunlight_id']
    else:
        cur.execute('INSERT INTO sunlight_value (value) VALUES (%s) RETURNING sunlight_id',
                    (value,))
        id = cur.fetchone()['sunlight_id']
    return id


if __name__ == '__main__':
    t1_start = perf_counter()
    load_dotenv('./.env') #remove before dockerising
    config = os.environ

    df = get_dataframe()
    df = clean_dataframe(df)
    #df = pd.read_csv('./clean.csv', na_filter=False) # remove me later TODO


    with get_db_connection(config) as conn, conn.cursor() as cur:
        for row in df.to_dict(orient="records"):

            # Check if failure or 7 if so continue
            if not (isinstance(row['name'], str) and row['name'] != 'NaN'):
                continue
            if row['name'] == '':
                continue

            continent_id = load_continents(row, cur)
            country_id = load_countries(continent_id, row, cur)
            plant_cycle_id = None
            if isinstance(row['plant_cycle'], str) and row['plant_cycle'] != '':
                plant_cycle_id = load_plant_cycles(row, cur)
            plant_id = load_plants(row, cur, plant_cycle_id, country_id)
            botanist_id = load_botanist(row, cur)

            if not isinstance(row['sunlight'], float):
                for sunlight_value in row['sunlight']:
                    load_sunlight_value(sunlight_value, cur)
            
        conn.commit()

    t1_stop = perf_counter()
    print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start)