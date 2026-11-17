# RESOLVERS GRAPHQL DU SERVICE LIEUX

# Imports
from geocoding import geocode, geocode_arr_dep
from database import parks_collection
from utils import find_nearest_park               


# Resolver de la requête geocode
# Test Insomnia : query { geocode(req: "gare de nantes") { label lat lon } }
def resolve_geocode(_, info, req):                          
    return geocode(req)                                     


# Resolver de la requête départ arrivée 
# Test Insomnia : query { geocode_arr_dep(start: "gare de nantes", end: "imt atlantique") { start { label lat lon } end { label lat lon } } }
def resolve_geocode_arr_dep(_, info, start, end):          
    return geocode_arr_dep(start, end)     


# Resolver de la requête get_parks
# Test Insomnia : query { get_parks { label lat lon } }
def get_parks(_, info):
    parks = list(parks_collection.find({}, {"_id": 0}))
    return parks      


# Resolver qui trouve le parc le plus proche du départ et de l'arrivée à partir de 4 coordonnées fournies représentant le départ et l'arrivée 
# Test Insomnia : query { get_nearest_park(start_lat: 47.2184, start_lon: -1.5536, end_lat: 47.2455, end_lon: -1.5584) { location { label lat lon } total_distance_km } }
def get_nearest_park(_, info, start_lat, start_lon, end_lat, end_lon):
    return find_nearest_park(start_lat, start_lon, end_lat, end_lon)


# Resolver qui trouve le parc le plus sur le trajet à partir du nom du lieu de départ et du nom du lieu d'arrivée 
# Test Insomnia : query { geocode_arr_dep(start: "gare de nantes", end: "imt atlantique") { start { label lat lon } end { label lat lon } nearest_park { location { label lat lon } total_distance_km } } }
def resolve_trip_nearest_park(trip, info):
    start, end = trip.get("start"), trip.get("end")
    if start is None or end is None:                                
        return None
    return find_nearest_park(start["lat"], start["lon"], end["lat"], end["lon"])