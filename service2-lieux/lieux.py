# SERVEUR FLASK DU SERVICE 2 (GRAPHQL)


# Imports
from flask import Flask, request, jsonify
from database import parks_collection, init_parks, toilets_collection, init_toilets
from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, QueryType, ObjectType, EnumType
from enums import LocationType
import resolvers as r       


# Création de l'application Flask
app = Flask(__name__)


# Serveur
PORT = 3002
HOST = '0.0.0.0'


# Binding GraphQL
type_defs = load_schema_from_path("lieux.graphql")   

location_type = EnumType("LocationType", LocationType)

query = QueryType()                                                
query.set_field("geocode", r.resolve_geocode)                     
query.set_field("geocode_arr_dep", r.resolve_geocode_arr_dep)   
query.set_field("get_locations", r.resolve_get_locations)   
query.set_field("get_nearest_location", r.resolve_get_nearest_location)    

trip = ObjectType("Trip")
trip.set_field("nearest_location", r.resolve_trip_nearest_location) 

schema = make_executable_schema(type_defs, query, trip, location_type)              


# Point d'entrée requêtes GraphQL
@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()                                        
    success, result = graphql_sync(schema, data)
    status_code = 200 if success else 400                         
    return jsonify(result), status_code                      


# Lancement du serveur Flask
if __name__ == "__main__":
   
   if parks_collection.count_documents({}) == 0:
       init_parks()

   if toilets_collection.count_documents({}) == 0:
       init_toilets()

   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
