"""contains functions to load data into database"""
import os
from time import perf_counter

from extract import get_dataframe, clean_dataframe
from database_connection import get_db_connection


def load_continents(record, cur) -> int:
    """loads continents into continent table and returns their id"""
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
    """loads countries into country table and returns their id"""
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
    """loads cycles into plant_cycle table and returns their id"""
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
    """loads plant data into plant table and returns their id"""
    name = record['name']
    cur.execute("SELECT * FROM plant WHERE name = %s", (name,))
    result = cur.fetchone()
    if result:
        id = result['plant_id']
    else:
        cur.execute('INSERT INTO plant (name, country_id, plant_cycle_id)\
                    VALUES (%s, %s, %s) RETURNING plant_id',
                    (name, country_id, plant_cycle_id,))
        id = cur.fetchone()['plant_id']
    return id


def load_botanist(record, cur) -> int:
    """loads botanists into botanist table and returns their id"""
    first_name = record['first_name']
    last_name = record['last_name']
    email = record['email']
    cur.execute("SELECT * FROM botanist WHERE first_name = %s AND last_name = %s",
                (first_name, last_name,))
    result = cur.fetchone()
    if result:
        id = result['botanist_id']
    else:
        cur.execute('INSERT INTO botanist (first_name, last_name, email)\
                    VALUES (%s, %s, %s) RETURNING botanist_id',
                    (first_name, last_name, email,))
        id = cur.fetchone()['botanist_id']
    return id


def load_sunlight_value(value, cur) -> int:
    """loads sunlight levels into sunlight_value table and returns their id"""
    value = str(value).lower().strip()
    # quick hack for fixing dodgy sunlight
    if value == "part sun/part shade":
        value = "part shade"
    cur.execute("SELECT * FROM sunlight_value WHERE value = %s", (value,))
    result = cur.fetchone()
    if result:
        id = result['sunlight_id']
    else:
        cur.execute('INSERT INTO sunlight_value (value) VALUES (%s) RETURNING sunlight_id',
                    (value,))
        id = cur.fetchone()['sunlight_id']
    return id


def load_record(record, cur, botanist_id, plant_id):
    """loads record data of plant in to record table"""
    recording_taken = record['recording_taken']
    last_watered = record['last_watered']
    soil_moisture = record['soil_moisture']
    temperature = record['temperature']
    cur.execute('INSERT INTO record (recording_taken, botanist_id, plant_id,\
                last_watered, soil_moisture, temperature) VALUES (%s,%s,%s,%s,%s,%s)',
                (recording_taken, botanist_id, plant_id, last_watered, soil_moisture, temperature,))


def load_sunlight_plant_link(cur, sunlight_id, plant_id):
    """links plant to sunlight value needed"""
    cur.execute("INSERT INTO sunlight_for_plant (plant_id, sunlight_id)\
                VALUES (%s, %s) ON CONFLICT DO NOTHING", (plant_id, sunlight_id,))


def handler(event, context):
    """lambda handler function"""
    t1_start = perf_counter()

    config = os.environ

    df = get_dataframe()
    df = clean_dataframe(df)


    with get_db_connection(config) as conn, conn.cursor() as cur:
        for row in df.to_dict(orient="records"):

            # Check if valid input, if not continue
            if not (isinstance(row['name'], str) and row['name'] != 'NaN'):
                print("Couldn't get plant data for: "+str(row['plant_id']))
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
                    sunlight_id = load_sunlight_value(sunlight_value, cur)

            load_record(row, cur, botanist_id, plant_id)
            load_sunlight_plant_link(cur, sunlight_id, plant_id)


        conn.commit()

    t1_stop = perf_counter()
    print("Time taken to extract, transform and load data:",
                                            t1_stop-t1_start)


if __name__ == "__main__":
    handler(None, None)
