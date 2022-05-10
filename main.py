# Food Pantry Locator App

import PySimpleGUI as sg

# Set the theme
sg.theme('Light Brown 8')

# LAYOUTS
user_input_layout = [
	[sg.Text('Please enter the following information:', font='Calibri 30')],
	[sg.Text('Address:', font='Calibri 20'), sg.In(size=(30,2), key='-ADDRESS-', font='Calibri 18'),
	 	sg.Text('City:', font='Calibri 20'), sg.Input(size=(20,2), key='-CITY-', font='Calibri 18')],
	[sg.Text('State:', font='Calibri 20'), sg.Input(default_text='NJ', size=(2,2), key='-STATE-', readonly=True, font='Calibri 18 bold', text_color="brown"),
		sg.Text('ZIP/Postal Code:', font='Calibri 20'), sg.Input(size=(7,2), key='-ZIP-', font='Calibri 18')],
	[sg.Text('Within:', font='Calibri 20'),
		sg.Radio('5 miles', 'MILES', default=True, font='Calibri 15', key='-FIVEMILES-'),
		sg.Radio('10 miles', 'MILES', font='Calibri 15', key='-TENMILES-'),
		sg.Radio('20 miles', 'MILES', font='Calibri 15', key='-TWENTYMILES-')],
	[sg.Submit(button_text='SEARCH', pad=(3, 10), font='Calibri 20', key='-SEARCH-'),
		sg.Button(button_text='RESET', pad=(3, 10), font='Calibri 20', key='-RESET-')]]

# Create the layout
layout = [[sg.Text('FOOD PANTRY LOCATOR', font='Calibri 40 bold')]] + user_input_layout + [[sg.HorizontalSeparator()]]


# Create the window
window = sg.Window('FOOD PANTRY LOCATOR', layout)

# Event loop to process "events" and get the "values" of the inputs
while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or click cancel
		break
	print('You Entered ', values[0])

window.close()