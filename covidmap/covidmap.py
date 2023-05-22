# Simple script to make a worldmap of covid cases to date.
# Relies on data from https://ourworldindata.org/covid-cases
# The direct DL is https://covid.ourworldindata.org/data/owid-covid-data.json

import json
import requests
import country_converter as coco
from pygal.maps.world import World
from pygal.style import Style
from datetime import date

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
		if country_code:
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

def make_categories():
	## Create a heatmap using the (max - min) cases / 5 categories
	interval_one = {}
	interval_two = {}
	interval_three = {}
	interval_four = {}
	interval_five = {}
	# now, we use math to get the limits for each interval
	overall_data = get_cases(load_data())
	max_cases = max(list(overall_data.values()))
	min_cases = min(list(overall_data.values()))
	interval = int((max_cases - min_cases)/5)
	# with that, we put countries into their intervals using their case count
	for key, value in overall_data.items():
		if value >= min_cases and value < min_cases + interval:
			interval_one[key] = value
		elif value >= min_cases + interval and value < min_cases + 2*interval:
			interval_two[key] = value
		elif value >= min_cases + 2*interval and value < min_cases + 3*interval:
			interval_three[key] = value
		elif value >= min_cases + 3*interval and value < min_cases + 4*interval:
			interval_four[key] = value
		elif value >= min_cases + 4*interval and value <= max_cases:
			interval_five[key] = value	
	return (max_cases, min_cases, interval, interval_one, interval_two, interval_three, interval_four, interval_five)

def make_svg():
	## Function to make the worldmap visual and save as covidmap.svg
	custom_style = Style(legend_font_size=12, colors=('#FFD970', '#FFBC0A', '#EC7D10', '#FF481F', '#FF0000'))
	(max_cases, min_cases, interval, i1, i2, i3, i4, i5) = make_categories()
	wm = World(style=custom_style)
	date_string = date.today().strftime("%B %d, %Y")
	wm.title = "COVID-19 Cases by Country as of " + str(date_string)
	wm.add(str(int(min_cases/1000000)) + ' - ' + str(int((min_cases + interval)/1000000)) + 'M cases', i1)
	wm.add(str(int((min_cases + interval)/1000000)) + ' - ' + str(int((min_cases + 2*interval)/1000000)) + 'M cases', i2)
	wm.add(str(int((min_cases + 2*interval)/1000000)) + ' - ' + str(int((min_cases + 3*interval)/1000000)) + 'M cases', i3)
	wm.add(str(int((min_cases + 3*interval)/1000000)) + ' - ' + str(int((min_cases + 4*interval)/1000000)) + 'M cases', i4)
	wm.add(str(int((min_cases + 4*interval)/1000000)) + ' - ' + str(int(max_cases/1000000)) + 'M cases', i5)
	wm.render_to_file('covidmap.svg')
	print("SVG saved. It is titled 'covidmap.svg'")

check_data_json() # first, we need data to feed into the script
check_mapping_json() # then, we need the country code mappings
make_svg() # finally, we can make the svg

