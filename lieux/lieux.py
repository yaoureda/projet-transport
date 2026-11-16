# Imports
from flask import Flask, request, jsonify
import requests
from database import parks_collection, init_parks
from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, QueryType
import resolvers as r       


# Création de l'application Flask
app = Flask(__name__)

# Serveur
PORT = 3002
HOST = '0.0.0.0'


# Binding GraphQL
type_defs = load_schema_from_path("lieux.graphql")                 
query = QueryType()                                                
query.set_field("geocode", r.resolve_geocode)                     
query.set_field("geocode_arr_dep", r.resolve_geocode_arr_dep)   
query.set_field("get_parks", r.get_parks)   
query.set_field("get_nearest_park", r.get_nearest_park)  
schema = make_executable_schema(type_defs, query)                 



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

   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
