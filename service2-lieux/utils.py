# FONCTIONS UTILES DU SERVICE 2


# Imports
from math import radians, sin, cos, asin, sqrt    


# Calcul la distance entre deux points de coordonnées
def distance(lat1, lon1, lat2, lon2):
    
    # Distance à vol d'oiseau en kilomètres
    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (sin(dlat / 2) ** 2
         + cos(radians(lat1)) * cos(radians(lat2))
         * sin(dlon / 2) ** 2)

    return 2 * R * asin(sqrt(a)) 


# Fonction qui trouve le lieu d'intéret le plus proche de deux points quelconques 
def find_nearest_location(collection, start_lat, start_lon, end_lat, end_lon):
    lieux = collection.find({}, {"_id": 0})

    nearest_location = None
    min_distance = float("inf")

    for lieu in lieux:
        lat = float(lieu["lat"])
        lon = float(lieu["lon"])

        d1 = distance(start_lat, start_lon, lat, lon)
        d2 = distance(lat, lon, end_lat, end_lon)

        total_distance = d1 + d2

        if total_distance < min_distance:
            min_distance = total_distance
            nearest_location = lieu

    if nearest_location is None:
        return None

    return {
        "location": nearest_location,
        "total_distance_km": round(min_distance, 2)
    }   