# RESOLVERS GRAPHQL DU GEOCODAGE

# Imports
from geocoding import geocode, geocode_arr_dep                


# Resolver de la requête geocode
def resolve_geocode(_, info, req):                          
    return geocode(req)                                     


# Resolver de la requête départ arrivée 
def resolve_geocode_arr_dep(_, info, start, end):          
    return geocode_arr_dep(start, end)                       