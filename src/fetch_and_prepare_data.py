import os
import json
import requests

def load_api_key() :
    with open("config.json") as f:
        config_json = json.load(f)
    return config_json['NINJAS_API_KEY']
        

def get_city_info(city_name, api_key):
    """
    Get geographical information about a city using the API Ninjas geocoding service.

    Parameters:
        city_name (str): Name of the city.
        api_key (str): API Key associated with the account.

    Returns:
        dict: Dictionary containing the city's name, latitude, longitude, and population.
    """
    api_url = f"https://api.api-ninjas.com/v1/city?name={city_name}"
    response = requests.get(api_url, headers={"X-Api-Key": api_key})
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

    data = response.json()[0]
    return [data["name"], data["longitude"], data["latitude"], data["population"]]

import csv
import argparse
import pandas as pd
import numpy as np

def process_city_data(input_file, api_key):
    """
    Process city data from input TXT and save results to output CSV.

    Parameters:
        input_file (str): Path to the TXT file containing names of cities.
        api_key (str): API Key associated with the account.
    """
    cities_list = []
    output_path = "data/full_data.csv"

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    with open(input_file, "r", encoding="utf-8") as f:
        city_names = [line.strip() for line in f.readlines()]
    
    for index, city_name in enumerate(city_names):
        try:
            print(f"Processing: {city_name}")
            city_info = get_city_info(city_name, api_key)
            cities_list.append(city_info)
        except Exception as e:
            print(f"Error processing {city_name}: {e}")
        
        if not index % 10:
            cities_data = pd.DataFrame(cities_list, columns=["name", "lon", "lat", "population"])
            cities_data.to_csv(output_path, index=False)
            print(f"Saved data to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Fetch city data and save to CSV.")
    parser.add_argument("input_file", type=str, help="Path to the txt file containing names of cities.")

    args = parser.parse_args()
    api_key = load_api_key()

    process_city_data(args.input_file, api_key)


if __name__ == "__main__":
    main()
