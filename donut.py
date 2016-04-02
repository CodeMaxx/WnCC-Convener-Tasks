'''This program will give you places arranged in ascending order
of their distance(by road) from IIT Bomay

Usage:
Place the input.txt file as the same folder as this.
Install the following depecdencies for python3:
1. urllib
2. simplejson
3. googlemaps
'''

from math import radians, cos, sin, asin, sqrt
import urllib.request as urlreq # Used to make an HTTP Request
import urllib.parse as urlparse # Used to create the proper URL using parameters
import operator #Has efficient functions for intrinsic operators
import simplejson as json # Used to parse the JSON Response
import googlemaps # Using this to get latitude and longitues(for Bonus Task)

DESTINATIONS = []
DISTANCES = {}
BIRD_VIEW = {}
CANT_FIND = {}

def get_destinations():
    '''Extracts the places, where we can buy sugar, from the input file'''

    file = open('input.txt', 'r')

    global DESTINATIONS
    # Getting the various places from input file
    DESTINATIONS = [x.strip('\n') for x in file.readlines()]

def get_distances():
    '''Gets distances of places from IIT Bombay using Google API'''

    gmaps = googlemaps.Client(key='AIzaSyDQdEGkpZybHE5PGbGWnh9ij5Q3GJTy2kc')
    iitb = gmaps.geocode('IIT Bombay')[0]['geometry']['location']

    data = {} #This stores the URL Parameters
    data['origin'] = 'IIT Bombay'

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
        # Getting latitude and longitude of destination
        position = gmaps.geocode(destination)[0]['geometry']['location']
        try:
            DISTANCES[destination] = float(routes[0]['legs'][0]
                                           ['distance']['text'][0:-3].replace(',', ''))
        except:
            CANT_FIND[destination] = int(haversine(iitb['lng'], iitb['lat'],
                                                   position['lng'], position['lat']))
        # Getting the Bird View Distance
        BIRD_VIEW[destination] = int(haversine(iitb['lng'], iitb['lat'],
                                               position['lng'], position['lat']))


def sort():
    '''Sorts the places according to their distance for IIT Bombay'''

    global CANT_FIND
    global BIRD_VIEW
    global DISTANCES
    # Sorting in ascending order of distances
    DISTANCES = sorted(DISTANCES.items(), key=operator.itemgetter(1))
    CANT_FIND = sorted(CANT_FIND.items(), key=operator.itemgetter(1))
    BIRD_VIEW = sorted(BIRD_VIEW.items(), key=operator.itemgetter(1))


def output():
    '''Outputs the result'''

    print("Take a Taxi(You know nothing Loca Cocinero) and visit the Sugar Suppliers in the order below:")
    for place in DISTANCES:
        print(place[0] + ' - ' + str(place[1]) + ' km')
    for place in CANT_FIND:
        print(place[0])

    print("\nThe Bird View Distances are:")
    for place in BIRD_VIEW:
        print(place[0] + ' - ' + str(place[1]) + ' km')

def haversine(lon1, lat1, lon2, lat2):
    '''Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)'''

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    abc = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    cde = 2 * asin(sqrt(abc))
    kms = 6367 * cde
    return kms

get_destinations()
get_distances()
sort()
output()
