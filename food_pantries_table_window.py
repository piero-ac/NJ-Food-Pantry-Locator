# File for creating the Table of Food Pantries
import json
import PySimpleGUI as sg
import address as addr
import haversine as hs
from haversine import Unit
from operator import itemgetter

# Function to traverse the JSON file and determine locations near the user's address
def build_table(user_lat, user_lon, search_range):
	locations_within_range = [] # List for food pantry locations within range

	# Obtain the user's coordinates
	user_coords = (user_lat, user_lon) 

	# Open the JSON file
	f = open('NJ_FP_locations.json')

	# Store the JSON as a Dictionary
	data = json.load(f)

	# Traverse each city entry's FP locations
	for city in data:
		# Get the keys (the city's food pantries)
		fp_list = data[city].keys() 

		# Traverse the values within each food pantry dictionary
		for key in fp_list:
			# Store the dictionary for the food pantry
			fp_info = data[city][key]

			# Save the current food pantry's name, address, telephone and coords
			name = key
			address = fp_info["full_address"]
			telephone = fp_info["telephone"]
			link = fp_info["link"]
			fp_coords = (fp_info["latitude"], fp_info["longitude"])

			# Calculate the distance from user to food pantry using the haversine module
			distance = hs.haversine(user_coords, fp_coords, unit=Unit.MILES)

			# If distance from each other within range, then append to list
			if distance <= search_range:
				locations_within_range.append([name, address, telephone, round(distance, 2)])

	# Close the file
	f.close()

	# Sort by nearest locations 
	locations_within_range = sorted(locations_within_range, key=itemgetter(3))
	return locations_within_range



def create(user_lat, user_lon, search_range):
	# Headings for Table
	headings = ['NAME', 'ADDRESS', 'PHONE NUMBER', 'DISTANCE (MILES)']

	# List holding food pantry locations
	locations = build_table(user_lat, user_lon, search_range)
	num_of_results = len(locations) # Number of locations near user

	food_pantries_table_window_layout = [
		[sg.Text(f"Search Resulted in {num_of_results} Food Pantry Locations", font="Calibri 25 bold")],
		[sg.Table(values=locations, headings=headings, max_col_width=35,
			auto_size_columns=True,
			justification='center',
			num_rows=10,
			key='-TABLE-',
			row_height=35,
			header_font='Calibri 20 bold',
			font='Calibri 15',
			alternating_row_color='#D2B48C',
			tooltip='Food pantry locations near you')]
	]

	food_pantries_window = sg.Window('Food Pantry Locations Window',
		food_pantries_table_window_layout, modal=True)

	while True:
		event, values = food_pantries_window.read()
		if event == "Exit" or event == sg.WIN_CLOSED:
			break

	food_pantries_window.close()

