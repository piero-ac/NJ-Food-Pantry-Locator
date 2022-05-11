# Module containg functions for validating addresses
# and getting coordinates for given address
import geopy
import geocoder
from geopy.geocoders import Nominatim


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
