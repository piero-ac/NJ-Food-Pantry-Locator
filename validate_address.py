# Module containg functions for validating the entered address
from pygeocoder import Geocoder

# Function to check for empty input fields
def empty_fields(user_info):
	if "" in user_info or None in user_info:
		return True
	
	return False

# Function to check for a valid address
# Returns a boolean
def validate(address):
	valid = Geocoder.geocode(address)
	return valid.valid_address
	# if valid.valid_address:
	# 	return valid.coordinates # return the coordinates for entered address

	# return False

# Function to get the coordinates for an address
# Returns a tuple containing (latitude, longitude)
def get_coordinates(address):
	coords = Geocoder.geocode(address).coordinates
	return coords


