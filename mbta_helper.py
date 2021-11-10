import urllib.request
import json
import pprint

MAPQUEST_API_KEY = "VfTg61yaL227a6A9zgMacxR5HaY5bbZF"
MBTA_API_KEY = "8f19cea60a5b4065b8bd78d9de73f830"

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """

    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return response_data

def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developer.mapquest.com/documentation/geocoding-api/address/get/
    for Mapquest Geocoding  API URL formatting requirements.
    """
    ' ' == ','
    MAPQUEST_URL = (get_json(f"http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}&location={place_name},Boston,MA"))
    lat_long = MAPQUEST_URL['results'][0]['locations'][0]['latLng']
    return tuple(lat_long.values())


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible)
    tuple for the nearest MBTA station to the given coordinates.
    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL
    formatting requirements for the 'GET /stops' API.
    """
    MBTA_URL = (get_json(f"https://api-v3.mbta.com/stops?api_key={MBTA_API_KEY}&sort=distance&filter%5Blatitude%5D={latitude}&filter%5Blongitude%5D={longitude}"))
    station_name = MBTA_URL['data'][0]['attributes']['name']
    wheelchair_accessible = MBTA_URL['data'][0]['attributes']['wheelchair_boarding']
    if wheelchair_accessible == 0:
        availabilty = "no wheelchair accessibility available" 
    elif wheelchair_accessible > 0:
        availabilty = "wheelchair accessibility available"
    return (f"{station_name} station has {availabilty}.")

def find_stop_near(place_name):
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.
    """
    latitude = get_lat_long(place_name)[0]
    longitude = get_lat_long(place_name)[1]
    return get_nearest_station(latitude, longitude)


def main():
    """
    You can test all the functions here
    """
    place_name = input("Please enter an address in Boston, to find an MBTA stop near you that is wheelchair accessible.\n")
    print(find_stop_near(place_name))
    




if __name__ == '__main__':
    main()
