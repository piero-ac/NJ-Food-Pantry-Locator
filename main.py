# Food Pantry Locator App

import PySimpleGUI as sg
import food_pantries_table_window
import address as addr

# Set the theme
sg.theme('Light Brown 8')

# Function to create layouts for search options
def create_search_layout(text, sub_text, input_key, input_width, button_key):
	layout = [
		[sg.Text(text, font='Calibri 25')],
		[sg.Text(sub_text, font='Calibri 18 italic')],
		[sg.In(size=(input_width,2), key=input_key, font='Calibri 18', justification="center")],
		[sg.Submit(button_text='SEARCH', pad=(3, 10), font='Calibri 20', key=button_key)]]

	return layout

# Function to find the selected search range for food pantry locations
def find_selected_range(values):
	if values['-FIVEMILES-']:
		return 5
	elif values['-TENMILES-']:
		return 10
	elif values['-TWENTYMILES-']:
		return 20

# Function to display popup when search is done with empty field
def error_popup(message):
	sg.Popup(message, font="Calibri 20 bold", text_color="red")

# Layouts for Search Options
search_by_city_layout = create_search_layout('Search by City', "Only Places in NJ", '-CITY-', 30, '-SEARCH_CITY-')
search_by_zipcode_layout =create_search_layout('Search by ZIP', "12345 or 12345-6789 or 12345 1234", '-ZIP-', 15, '-SEARCH_ZIP-')

# Layout for Search Range Selection
choose_range_layout = [
	[sg.Text('Within:', font='Calibri 20'),
		sg.Radio('5 miles', 'MILES', default=True, font='Calibri 15', key='-FIVEMILES-'),
		sg.Radio('10 miles', 'MILES', font='Calibri 15', key='-TENMILES-'),
		sg.Radio('20 miles', 'MILES', font='Calibri 15', key='-TWENTYMILES-')]]

# Create the layout for the window
layout = [[sg.Text('FOOD PANTRY LOCATOR', font='Calibri 40 bold')]] + search_by_city_layout + [[sg.HorizontalSeparator()]] + search_by_zipcode_layout + [[sg.HorizontalSeparator()]] + choose_range_layout


# Create the window
window = sg.Window('FOOD PANTRY LOCATOR', layout, element_justification='center')

# Event loop to process "events" and get the "values" of the inputs
while True:
	event, values = window.read()

	# Event: user closes window
	if event == sg.WIN_CLOSED: 
		break
		
	# Event: user searches by city
	elif event == '-SEARCH_CITY-':
		city_info = values['-CITY-'].strip()
		search_range = find_selected_range(values)

		if not city_info:
			error_popup("CITY FIELD EMPTY")
			continue # Halt search and make user try again

		# validate city
		city_info = addr.validate_city(city_info)

		if city_info == "Invalid":
			error_popup("INVALID CITY\nEnsure you entered a valid city")
			continue # Halt search and make user try again

		# get the coordinates for the city
		user_lat, user_lon = addr.get_coordinates(city_info)

		# Create window of food pantries within search range
		food_pantries_table_window.create(user_lat, user_lon, search_range)

	# Event: user searches by zip
	elif event == '-SEARCH_ZIP-':
		zip_info = values['-ZIP-'].strip()
		search_range = find_selected_range(values)

		if not zip_info:
			error_popup("ZIP FIELD EMPTY")
			continue # Halt search and make user try again

		# validate zipcode 
		zip_info = addr.validate_ZIPCODE(zip_info)

		if zip_info == "Invalid":
			error_popup("INVALID ZIPCODE")
			continue # Halt search and make user try again

		# get the coordinates for the ZIPCODE (latitude, longitude)
		user_lat, user_lon = addr.get_coordinates("NJ " + zip_info)

		# Create window of food pantries within search range
		food_pantries_table_window.create(user_lat, user_lon, search_range)


window.close()