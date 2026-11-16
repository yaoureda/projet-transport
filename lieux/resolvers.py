# RESOLVERS GRAPHQL DU GEOCODAGE

# Imports
from geocoding import geocode, geocode_arr_dep                


# Resolver de la requête geocode
# Test Insomnia : query { geocode(req: "gare de nantes") { label lat lon } }
def resolve_geocode(_, info, req):                          
    return geocode(req)                                     


# Resolver de la requête départ arrivée 
# Test Insomnia : query { geocode_arr_dep(start: "gare de nantes", end: "imt atlantique") { start { label lat lon } end { label lat lon } } }
def resolve_geocode_arr_dep(_, info, start, end):          
    return geocode_arr_dep(start, end)                       