# RESOLVERS GRAPHQL DU SERVICE 2 

# Imports
from geocoding import geocode, geocode_arr_dep
from utils import find_nearest_location
from database import COLLECTIONS


# Resolver de la requête geocode
# Test Insomnia : query { geocode(req: "gare de nantes") { label lat lon } }
def resolve_geocode(_, info, req):                          
    return geocode(req)                                     


# Resolver de la requête départ arrivée 
# Test Insomnia : query { geocode_arr_dep(start: "gare de nantes", end: "imt atlantique") { start { label lat lon } end { label lat lon } } }
def resolve_geocode_arr_dep(_, info, start, end, type=None):          
    trip = geocode_arr_dep(start, end)
    if trip is None:
        return None
    trip["type"] = type
    return trip  


# Resolver de la requête get_locations
# Test Insomnia : query { get_locations(type: PARK) { label lat lon } }
def resolve_get_locations(_, info, type):
    collection = COLLECTIONS[type]
    return list(collection.find({}, {"_id": 0}))     


# Resolver qui trouve le parc le plus proche du départ et de l'arrivée à partir de 4 coordonnées fournies représentant le départ et l'arrivée 
# Test Insomnia : query { get_nearest_location(type: PARK, start_lat: 47.2184, start_lon: -1.5536, end_lat: 47.2455, end_lon: -1.5584) { location { label lat lon } total_distance_km } }
def resolve_get_nearest_location(_, info, type, start_lat, start_lon, end_lat, end_lon):
    collection = COLLECTIONS[type]
    return find_nearest_location(collection, start_lat, start_lon, end_lat, end_lon)


# Resolver qui trouve le parc le plus sur le trajet à partir du nom du lieu de départ et du nom du lieu d'arrivée 
# Test Insomnia : query { geocode_arr_dep(start: "gare de nantes", end: "imt atlantique", type: TOILET) { start { label lat lon } end { label lat lon } nearest_location { location { label lat lon } total_distance_km } } }
def resolve_trip_nearest_location(trip, info):
    start, end, type = trip.get("start"), trip.get("end"), trip.get("type")
    if start is None or end is None or type is None:                                
        return None
    collection = COLLECTIONS[type]
    return find_nearest_location(collection, start["lat"], start["lon"], end["lat"], end["lon"])