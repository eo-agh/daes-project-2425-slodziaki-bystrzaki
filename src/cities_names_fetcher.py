import os
import json
import requests

def load_api_username() :
    with open("config.json") as f:
        config_json = json.load(f)
    return config_json['GEONAMES_USERNAME']
        

def get_country_info(number_of_countries, username):
    """
    Get a list of countries and their population from the geonames API, 
    filtered to include only countries in North America, South America, Europe, and Asia.

    Parameters:
        number_of_countries (int): Number of countries to return information about.
        username (str): Username associated with the account.

    Returns:
        list of dicts: A sorted list of dictionaries containing:
            - countryName (str): Name of the country,
            - countryCode (str): Alpha-2 country code,
            - population (str): Population of the country.
    """
    url = "http://api.geonames.org/countryInfoJSON"
    params = {"username": username}
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")
    
    countries = response.json().get("geonames", [])
    
    countries_info = []

    for i in range(number_of_countries):
        if countries[i]["continent"] in ['NA', 'SA', 'EU', 'AS']:
            countries_info.append({
                "countryName": countries[i]["countryName"],
                "countryCode": countries[i]["countryCode"],
                "population": countries[i]["population"]
            })

    return sorted(countries_info, key=lambda x: int(x['population']), reverse = True)

def get_cities_names(country_code, amount, username):
    """
    Get the largest cities in a given country based on population, using the geonames API service.

    Parameters:
        country_code (str): Alpha-2 country code.
        amount (int): Number of cities to get.
        username (str): Username associated with the account.

    Returns:
        list: A list of city names ordered by population.
    """
    url = "http://api.geonames.org/searchJSON"
    params = {
        "country": country_code,
        "featureClass": "P",
        "orderby": "population",
        "maxRows": amount,
        "username": username
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")
    
    data = response.json().get("geonames", [])
    cities = [city["name"] for city in data]
    
    return cities

import csv
import pandas as pd
import numpy as np

def main():

    api_username = load_api_username()
    cities_amount_from_one_country = 30
    number_of_countries = 60
    cities = []

    for country_info in get_country_info(number_of_countries, api_username):
        cities.extend(get_cities_names(country_info["countryCode"], cities_amount_from_one_country, api_username))

    with open('data/cities_generated.txt', 'w', encoding='utf-8') as file:
        for line in cities:
            file.write(f"{line}\n")


if __name__ == "__main__":
    main()
