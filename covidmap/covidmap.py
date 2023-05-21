# Simple script to make a worldmap of covid cases to date.
# Relies on data from https://ourworldindata.org/covid-cases
# The direct DL is https://covid.ourworldindata.org/data/owid-covid-data.json

import json
import requests
import country_converter as coco
from pygal.maps.world import World

def get_country_code(name):
	## Reads mappings.json to get the existing dictionary of country codes.
	with open('mappings.json') as mappings:
			contents = json.load(mappings)
			for key, value in contents.items():
				if name == key and value != 'not found': # the passed in name must match a key in the dictionary, and have a value != 'not found'
					print("The name of the country is " + name + " which matches with key " + key + ". The value is " + value)
					return value
			print(name + " has no corresponding key or valid value in the mapping") # otherwise, if either condition not met, return None
			return None

def load_data(filename='owid-covid-data.json'):
	## Function to load a dataset into a variable
	try:
		with open(filename) as file:
			dataset = json.load(file)
			return dataset
	except:
		print("'owid-covid-data.json' could not be loaded.")
		quit()

def get_cases(dataset):
	## Function to loop through dataset and extract the country name and number of cases
	overall_data={} # set a blank dictionary first
	list_of_countries = list(dataset.keys()) # gets the list of countries in the dataset
	for keys, values in dataset.items(): # values is the dictionary assigned to each country
		country_code = get_country_code(keys)
		for country in list_of_countries:
			cases = 0 # first make a blank variable per run
			data = values['data'] # the data we want is in the list paired to key 'data'
			for each in data:
				try:
					cases = cases + int(each['new_cases']) # add the new_cases value to the cases variable
				except KeyError:
					pass
		overall_data[country_code] = cases # add the pygal code and cases value to the dictionary
	return overall_data

def check_mapping_json():
	## Checks whether a mappings.json is present, and if not, creates it
	try: # if the file exists, just move on
		with open ('mappings.json') as mappings:
			pass 
	except FileNotFoundError: # but if the file does not exist, then create it, and write the mappings dictionary to it
		print("'mappings.json' not found, creating now...")
		mapping_dict = {}
		dataset = load_data()
		for each in dataset.keys():
			mapping_dict[each] = str(coco.convert(names=each, to='ISO2').lower())
		with open('mappings.json', 'w') as mappings:
			json.dump(mapping_dict, mappings)

def check_data_json():
	## Checks whether the dataset is present, and if not, downloads it
	try: # if the file exists, just move on
		with open ('owid-covid-data.json') as data:
			pass 
	except FileNotFoundError: # but if the file does not exist, then download it
		try:
			print("'owid-covid-data.json' was not found, downloading now...")
			url = 'https://covid.ourworldindata.org/data/owid-covid-data.json'
			r = requests.get(url, allow_redirects=True)
			open('owid-covid-data.json', 'wb').write(r.content)
		except:
			print('Could not download.')
			quit()

def make_svg():
	## Function to make the worldmap visual and save as covidmap.svg
	wm = World()
	wm.title = "COVID-19 Cases by Country"
	wm.add('Cases', get_cases(load_data()))
	wm.render_to_file('covidmap.svg')
	print("SVG saved. It is titled 'covidmap.svg'")

check_data_json() # first, we need data to feed into the script
check_mapping_json() # then, we need the country code mappings
make_svg() # finally, we can make the svg

