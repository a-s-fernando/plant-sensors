import pandas as pd

def get_comprehensive_plants():
    plant_df = pd.read_csv('data/c7-aaa-s3-bucket/plant.csv')
    plant_cycle_df = pd.read_csv('data/c7-aaa-s3-bucket/plant_cycle.csv')

    plants_and_cycle_df = pd.merge(plant_df, plant_cycle_df, left_on="plant_cycle_id", right_on="plant_cycle_id", how="left")
    plants_and_cycle_df = plants_and_cycle_df.rename(columns={"value": "plant_cycle"}).drop("plant_cycle_id", axis=1)

    country_df = pd.read_csv('data/c7-aaa-s3-bucket/country.csv')
    continent_df = pd.read_csv('data/c7-aaa-s3-bucket/continent.csv', na_filter=False)

    country_continent_df = pd.merge(country_df, continent_df, left_on="continent_id", right_on="continent_id", how="inner")
    country_continent_df = country_continent_df.rename(columns={"name_x": "country", "name_y": "continent"}).drop("continent_id", axis=1)

    plants_and_country_df = pd.merge(plants_and_cycle_df, country_continent_df, left_on="country_id", right_on="country_id", how="left")
    plants_and_country_df = plants_and_country_df.drop('country_id', axis=1)

    record_df = pd.read_csv('data/c7-aaa-s3-bucket/record.csv')
    botanist_df = pd.read_csv('data/c7-aaa-s3-bucket/botanist.csv')
    records_with_botanists_df = pd.merge(record_df, botanist_df, left_on="botanist_id", right_on="botanist_id", how="left")
    records_with_botanists_df = records_with_botanists_df.drop("botanist_id", axis=1).rename(columns={"first_name":"botanist_fn","last_name":"botanist_ln","email":"botanist_email"})

    return pd.merge(records_with_botanists_df, plants_and_country_df, how="inner", left_on="plant_id", right_on="plant_id")

def get_combined_sunlight():
    sunlight_for_plant_df = pd.read_csv('data/c7-aaa-s3-bucket/sunlight_for_plant.csv')
    sunlight_value_df = pd.read_csv('data/c7-aaa-s3-bucket/sunlight_value.csv')
    combined_sunlight_df = pd.merge(sunlight_for_plant_df, sunlight_value_df, left_on="sunlight_id", right_on="sunlight_id", how="left")
    return combined_sunlight_df.rename(columns={"value": "sunlight"}).drop("sunlight_id", axis=1)
    # Leaving this as separate from the main plants df to avoid duplicates