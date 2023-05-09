import requests
from time import perf_counter
import pandas as pd

def get_data() -> list[dict]:
    '''Retrieves plants data'''

    data = []
    for i in range(50):
        url = f'https://data-eng-plants-api.herokuapp.com/plants/{i}'
        response = requests.get(url)
        data.append(response.json())
    
    return data


def get_countries():
    '''Retrieves dict for country codes mapping.'''

    url = 'http://country.io/names.json'
    response = requests.get(url)
    countries = response.json()

    return countries


def get_continents():
    '''Retrieves dict for continent codes mapping.'''

    url = 'http://country.io/continent.json'
    response = requests.get(url)
    continents = response.json()

    return continents


def get_dataframe():
    '''Load data into pandas dataframe'''

    data = get_data()
    df = pd.DataFrame(data)

    return df


def split_names(x):
    '''split first and last names'''

    if isinstance(x, dict):
        # print(x['name'], len(x['name'].split(' ')))
        return x['name'].split(' ')
    else:
        return [None, None]


def clean_dataframe(df): 
    '''Clean up dataframe'''

    countries = get_countries()
    continents = get_continents()

    df['first_name'] = df['botanist'].apply(split_names).apply(lambda x: x[0])
    df['last_name'] = df['botanist'].apply(split_names).apply(lambda x: x[1])

    df['email'] = df['botanist'].str['email']

    df = df.drop('images', axis=1)

    df['recording_taken'] = pd.to_datetime(df['recording_taken'])
    df['last_watered'] = pd.to_datetime(df['last_watered'])

    df = df.rename(columns={'origin_location': 'origin_country'})

    df['origin_country'] = df['origin_country'].str[3]

    df['origin_continent'] = df['origin_country'].replace(continents)

    df['origin_country'] = df['origin_country'].replace(countries)

    return df


if __name__ == '__main__':
    t1_start = perf_counter()
    df = get_dataframe()
    print(clean_dataframe(df))
    t1_stop = perf_counter()
    print("Elapsed time during the whole program in seconds:",
                                            t1_stop-t1_start)