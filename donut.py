'''This program will give you places arranged in ascending order
of their distance(by road) from IIT Bomay

Usage:
Place the input.txt file as the same folder as this.
Install the following depecdencies for python3:
1. urllib
2. simplejson
'''


import urllib.request as urlreq # Used to make an HTTP Request
import urllib.parse as urlparse # Used to create the proper URL using parameters
import operator #Has efficient functions for intrinsic operators
import simplejson as json # Used to parse the JSON Response

DESTINATIONS = []
DISTANCES = {}
EASY_SUGAR = []

def get_destinations():
    '''Extracts the places, where we can buy sugar, from the input file'''

    file = open('input.txt', 'r')

    global DESTINATIONS
    # Getting the various places from input file
    DESTINATIONS = [x.strip('\n') for x in file.readlines()]

def get_distances():
    '''Gets distances of places from IIT Bombay using Google API'''

    data = {} #This stores the URL Parameters
    data['origin'] = 'Indian Institute of Technology Bombay'

    # Creating URL for each place, then fetching and parsing data to get distances.
    for destination in DESTINATIONS:
        data['destination'] = destination
        request_values = urlparse.urlencode(data)
        # The request URL
        request = "https://maps.googleapis.com/maps/api/directions/json?" + request_values
        # Fetching the response
        string = urlreq.urlopen(request).read().decode('utf-8')
        # Extracting distance from the response
        routes = json.loads(string)['routes']
        try:
            DISTANCES[destination] = routes[0]['legs'][0]['distance']['text']
        except:
            print("Google Maps can't find distance from IIT Bombay to " + destination)

def sort():
    '''Sorts the places according to their distance for IIT Bombay'''

    global EASY_SUGAR
    # Sorting in ascending order of distances
    EASY_SUGAR = sorted(DISTANCES.items(), key=operator.itemgetter(1), reverse=True)

def output():
    '''Outputs the result'''

    print("\nTake a Taxi(You know nothing Loca Cocinero) and \
        visit the Sugar Suppliers in the following order:")
    for place in EASY_SUGAR:
        print(place[0])

get_destinations()
get_distances()
sort()
output()
