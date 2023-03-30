
import requests
import json


def set_up_countries(path):
    data = requests.get('https://countriesnow.space/api/v0.1/countries').json()
    countries_dict = {}
    countries = data['data']  # first we access the data
    for country in countries: # now we loop the countries
      countries_dict[country['country']] = country['cities']


    with open(path, "w") as f:
        json.dump(countries_dict, f)

