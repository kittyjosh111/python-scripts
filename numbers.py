import json

'''
Simple script that takes keeps prompting the user to input a username, which is then linked to their favorite number in
a dictionary, saved to a local numbers.json. If the username is again typed, it will display the favorite number.
This script is meant to provide an example of:
	try, except block
	if loop, and an if True style block
	while (infinite) loop
	dictionaries: keys, values
	factoring of code into functions
	write() and read(), and how json.dump() or json.load() preserves type
	input
'''

def check_json():
	""" Checks whether a numbers.json is present, and if not, creates it """
	try: #If the file exists, just move on.
		with open ('numbers.json') as numbers_json:
			pass 
	except FileNotFoundError: #But if the file does not exist, then create it, and write a blank dictionary to it.
		initial_dictionary = {}
		with open('numbers.json', 'w') as numbers_json:
			numbers_json.write('') #This creates the json file...
			json.dump(initial_dictionary, numbers_json) #And this writes the above blank dict to it.

def get_numbers():
	""" Reads numbers.json to get the existing dictionary of numbers. Returns the dictionary. """
	check_json() #first check if numbers.json is present.
	with open('numbers.json') as numbers_json:
			contents = json.load(numbers_json)
			return contents #return the dictionary for use in further scripting.

def save_numbers(username, user_input):
	""" Writes a new username:user_input pair to the dictionary after running get_numbers() """
	dictionary = get_numbers() #gets the dictionary of numbers from number.json
	dictionary[username] = user_input #appends to dictionary in form username:user_input
	with open('numbers.json', 'w') as numbers_json:
		json.dump(dictionary, numbers_json)
		
def greet_user():
	""" Greeting for the user. Asks for username, then follows logic """
	while True: #infinite loop
		existing_dict = get_numbers() #first load in the existing dictionary, which runs get_numbers(). This triggers check_json too.
		username = input("\nHello! Please input your username. If you don't have one yet, type in a new username to create.\nType 'quit' to quit the program.\n")
		if username: #if the username exists...
			if username.lower() == 'quit': #this is how to break the infinite loop. Its first because it has more priority
				print("Goodbye!")
				break
			elif username in existing_dict.keys(): #check only the keys for the dictionary
				print("Hello again " + username + "!")
				if username in get_numbers():
					print("Your favorite number was: " + existing_dict[username]) #get the value from the key
			else:
				print("Hello " + username + ". Your account has been saved.")
				user_input = str(input("Please enter your favorite number below:\n"))
				save_numbers(username, user_input) #calls save_numbers
				print("Alright. Your favorite number of " + user_input + " has been saved.")
		else:
			print("Please enter your username:\n") #prompt user to actually put in something as their username.

greet_user()