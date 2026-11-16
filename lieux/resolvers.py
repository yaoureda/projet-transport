# RESOLVERS GRAPHQL DU GEOCODAGE

# Imports
from geocoding import geocode, geocode_arr_dep
from utils import distance
from database import parks_collection                


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

# Resolver pour GET le park le plus proche du départ et l'arrivée
# Test Insomnia : query { get_nearest_park(start_lat: 47.2184, start_lon: -1.5536, end_lat: 47.2455, end_lon: -1.5584) { location { label lat lon } total_distance_km } }
def get_nearest_park(_, info, start_lat, start_lon, end_lat, end_lon):
    parks = parks_collection.find({}, {"_id": 0})

    nearest_park = None
    min_distance = float("inf")

    for park in parks:
        lat = float(park["lat"])
        lon = float(park["lon"])

        d1 = distance(start_lat, start_lon, lat, lon)
        d2 = distance(lat, lon, end_lat, end_lon)

        total_distance = d1 + d2

        if total_distance < min_distance:
            min_distance = total_distance
            nearest_park = park

    if nearest_park is None:
        return None

    return {
        "location": nearest_park,
        "total_distance_km": round(min_distance, 2)
    }   
