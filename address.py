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
def validate_ZIP(postal_code):
	zipcode = re.compile("^\d{5}(?:[-\s]\d{4})?$")
	if zipcode.match(postal_code):
		return postal_code
	else:
		return "Invalid"


