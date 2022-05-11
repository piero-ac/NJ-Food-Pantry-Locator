# Module for input validations and formatting
import geopy
import geocoder
from geopy.geocoders import Nominatim
import re

# Function to check for a valid address
# Returns false if no result could be found
def validate(address):
	valid = geocoder.google(address, key="AIzaSyAzboXO3ZMju2Txx4owH64X8l6B8PqVRRA")
	return valid.ok

# Function to get the coordinates for an address
# Returns the latitude and longitude
def get_coordinates(address):
	loc = Nominatim(user_agent="GetLoc")
	get_loc = loc.geocode(address)
	return get_loc.latitude, get_loc.longitude

# Function to see if ZIP satisfies one of the following formats:
# 1) 12345   2) 12345-6789  3) 12345 1234
def validate_ZIPCODE(postal_code):
	zipcode = re.compile("^\d{5}(?:[-\s]\d{4})?$")
	if zipcode.match(postal_code):
		return postal_code
	else:
		return "Invalid"

# Function to see if city exists in NJ
def validate_city(city):
	# add the state to ensure, 
	# returned coordinates is for city in NJ
	if "NJ" not in city:
		city += ", NJ"

	# List to hold cities
	cities = []
	with open("cities.txt", "r") as f:
		cities = f.readlines()

	# Remove newline char for every entry
	cities = [x.strip() for x in cities]

	if city in cities:
		return city
	else:
		return "Invalid"


