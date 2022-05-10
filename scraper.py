# Food Pantry Website Scraper
# Module for scraping together the food pantry locations and their information
# from the website: https://www.foodpantries.org/st/new_jersey
# and creating a JSON file from that info

# Imports 
from bs4 import BeautifulSoup
import urllib.request
import re
import json
from address import get_coordinates



# Step 1. Access the food pantry website

food_pantry_website = urllib.request.urlopen("https://www.foodpantries.org/st/new_jersey")
fp_soup = BeautifulSoup(food_pantry_website, "html.parser")

# Step 2. Get the links from the anchor elements in the page
# But only those that point to New Jersey cities 
# and save to a text file for further use

city_links_file = open("city_links.txt", "w")
city_link_substring = "https://www.foodpantries.org/ci/nj-"
for a in fp_soup.findAll('a'):
	link = a.get('href') # Get the href value (link) of the anchor element
	if city_link_substring in link:
		city_links_file.write(f"{link}\n") # Write the link to file
city_links_file.close() # Close the file

# Step 3. Attain all of the links for the food pantries in New Jersey

food_pantry_links = open('fp_links.txt', 'w')
fp_link_substring = "https://www.foodpantries.org/li/"
fp_links_file = open("fp_links.txt", "w")

# Open the file and read the links 
with open("city_links.txt", "r") as f:
	attained_links = [] # list to store attained links

	for link in f:
		if link != "":
			link = link.strip() # Remove whitespaces from link
			city_name = link[34:] # Get the city name from the link

			# Access the city's website of food pantries
			city_fp_website = urllib.request.urlopen(link)
			city_fp_soup = BeautifulSoup(city_fp_website, "html.parser")

			# Traverse the anchor elements in the link
			for a in city_fp_soup.findAll('a'):
				fp_link = a.get('href') # Get the href value (link) of the anchor element

				if (fp_link_substring in fp_link) and (fp_link not in attained_links):
					print("attained: ", fp_link)
					fp_links_file.write(f"{fp_link}\n") # Write the link to file
					attained_links.append(fp_link) # To prevent having repeated links in the text file

fp_links_file.close()

"""
Step 4. Get the food pantry locations from each city and create a dictionary
containing dictionaries for every city's food pantries ex:
locations = {
	# City in NJ
	"City" : {
		# Food Pantries in City
		"abc food pantry" : {
			"telephone" : "123-123-1233"
			"address" : "123 das ave",
			"link" : "www.fp.org"
		}
	}
}

Then, convert the created the dictionary into a JSON file for use in the GUI Application
"""
# Function to extract Food Pantry's name, address, and telephone
# Returns a list with the city, food pantry's name, and
# dictionary containing the food pantry's telephone, address, and link 

def getInfoFromScriptTag(link_JSON, link):
	JSON = json.loads(link_JSON.string) # Get the script's JSON
	name = JSON["name"]
	telephone = JSON["telephone"]
	full_address, street, city, state, postal_code = getAddressFromScriptTag(JSON)

	# Use the state variable to check whether the food pantry
	# is located in NJ
	if state != "NJ":
		return False # Do not add to dictionary for city
	else:
		# Return a list with the city name and dictionary containing fp's info
		return [city,
			 	name, { 
			 	"telephone" : telephone, 
			 	"full_address" : full_address,
			 	"street" : street,
			 	"city" : city,
			 	"state" : state,
			 	"postal_code" : postal_code,
			 	"link" : link}] 

# Helper function to attain address from JSON
# Returns the city name, the compiled address, and state

def getAddressFromScriptTag(JSON):
	street = JSON["address"]["streetAddress"]
	city = JSON["address"]["addressLocality"]
	state = JSON["address"]["addressRegion"]
	postal_code = JSON["address"]["postalCode"]
	full_address = f"{street}, {city}, {state}, {postal_code}"
	return full_address, street, city, state, postal_code



NJ_FP_locations = {}

# Open the file and read the links 
with open("fp_links.txt", "r") as f:

	for link in f:
		if link != "":
			print(f"Analyzing: {link}")
			link = link.strip()
			fp_website = urllib.request.urlopen(link)
			fp_soup = BeautifulSoup(fp_website, "html.parser")

			# Find all script tags in the page with type: application/ld+json
			script_tags = fp_soup.findAll('script', type="application/ld+json")
			script_tag = script_tags[2] # The third script tag in the site contains the info we need

			# Call the getInfoFromScriptTag Function to populate 
			# the NJ_FP_locations dictionary with each food pantry's info
			try:
				fp_info = getInfoFromScriptTag(script_tag, link)
			except json.decoder.JSONDecodeError:
				print(f"SKIPPED: {link} DUE TO JSON PARSING ERROR")
				continue # Move on to the next link

			if fp_info:
				city = fp_info[0]
				fp_name = fp_info[1]
				details = fp_info[2]

				try:
					lat,lon = get_coordinates(details["full_address"])
				except AttributeError:
					try:
						short_address = f'{details["city"]}, {details["state"]}, {details["postal_code"]}'
						lat,lon = get_coordinates(short_address)
					except AttributeError:
						continue # If short address throws error, then don't add food pantry to json

				# Create keys for the latitude and longitude
				details["latitude"] = lat
				details["longitude"] = lon

				# Check if city is not a key in the dictionary
				if city not in NJ_FP_locations:
					# Then, create a key using the city name and append the food pantry
					NJ_FP_locations[city] = { fp_name : details}
				else:
					#Otherwise, append the next food pantry location to the city
					NJ_FP_locations[city][fp_name] = details
			print(f"Analyzed: {link}\n")

# Convert the dictionary to a JSON file
with open("NJ_FP_locations.json", "w") as f:
	json.dump(NJ_FP_locations, f)


"""
Summary of Steps 1-3: Steps 1-3 allowed me to obtain the individual links 
for the food pantries in New Jersey and create text files to avoid overloading
the website with requests every time the app would run

Summary of Step 4: I was able to obtain a JSON file that contains entries for each city 
in NJ that has a food pantry and within each city entry, the food pantries within that city.

For example, for Aberdeen the JSON file has the following entry:
"Aberdeen": {
		"Matawan United Methodist Pantry": {
			"telephone": "(732) 566-2996",
			"full_address": "478 Atlantic Av, Aberdeen, NJ, 07747",
			"street": "478 Atlantic Av",
			"city": "Aberdeen",
			"state": "NJ",
			"postal_code": "07747",
			"link": "https://www.foodpantries.org/li/nj_07747_matawan-united-methodist-pantry",
			"latitude": 40.408568,
			"longitude": -74.224138
		},
		"St. Joseph Church Pantry": {
			"telephone": "(732) 290-1878",
			"full_address": "42 Wooley Street, Aberdeen, NJ, 07747",
			"street": "42 Wooley Street",
			"city": "Aberdeen",
			"state": "NJ",
			"postal_code": "07747",
			"link": "https://www.foodpantries.org/li/nj_st-joseph-church-pantry",
			"latitude": 40.423378421262356,
			"longitude": -74.2135786873091
		}
	}
""" 