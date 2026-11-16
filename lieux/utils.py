
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