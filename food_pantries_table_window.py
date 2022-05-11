# File for creating the Table of Food Pantries
import json
import PySimpleGUI as sg
import haversine as hs
from haversine import Unit
from operator import itemgetter
import webbrowser

# Function to traverse the JSON file and determine locations near the user's address
def build_table(user_lat, user_lon, search_range):
	locations_within_range = [] # List for food pantry locations within range
	links_for_locations = [] # List for food pantries' website link

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
				links_for_locations.append([link,round(distance, 2)])

	# Close the file
	f.close()

	# Sort by nearest locations 
	try:
		locations_within_range = sorted(locations_within_range, key=itemgetter(3))
		links_for_locations = sorted(links_for_locations, key=itemgetter(1))
	except IndexError: 
		# IndexError thrown if no locations were added
		# This means the city/zipcode entered does not have any food pantry
		# locations within the selected range
		return [], []
	return locations_within_range, links_for_locations


# Function for creating the window displaying the table of results
def create(user_lat, user_lon, search_range):
	# Headings for Table
	headings = ['NAME', 'ADDRESS', 'PHONE NUMBER', 'DISTANCE (MILES)']

	# List holding food pantry locations
	locations, links = build_table(user_lat, user_lon, search_range)
	num_of_results = len(locations) # Number of locations near user
	table_clickable = True # Table can cause event

	# If locations is empty, then show empty table
	# and prevent table from causing event
	if len(locations) == 0:
		locations = [["N/A", "N/A", "N/A", "N/A"]]
		table_clickable= False

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
			tooltip='Food pantry locations near you',
			enable_events=table_clickable)]
	]

	food_pantries_window = sg.Window('Food Pantry Locations Window',
		food_pantries_table_window_layout, modal=True)

	while True:
		event, values = food_pantries_window.read()

		# Event: user exits the table window
		if event == "Exit" or event == sg.WIN_CLOSED:
			break

		# Event: user clicks on row to open link
		elif event == "-TABLE-":
			# Get the row that was clicked
			row_clicked = values["-TABLE-"][0]
			food_pantry_link = links[row_clicked][0] # link is in the first index
			webbrowser.open(food_pantry_link) # open the link user webbrowser library
			continue

	food_pantries_window.close()

