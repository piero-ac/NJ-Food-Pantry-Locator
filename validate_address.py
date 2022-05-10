# Module containg functions for validating the entered address
from pygeocoder import Geocoder
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy import distance

API_KEY = "AIzaSyAzboXO3ZMju2Txx4owH64X8l6B8PqVRRA"

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
# Returns the latitude and longitude
def get_coordinates(address):
	loc = Nominatim(user_agent="GetLoc")
	get_loc = loc.geocode(address)
	
	return get_loc.latitude, get_loc.longitude

# coords = get_coordinates("Hackettstown, NJ 07840")

# print(coords)
