# Imports
from flask import Flask, request, jsonify, make_response
from math import radians, sin, cos, asin, sqrt
import requests
from database import parks_collection, init_parks

# Création de l'application Flask
app = Flask(__name__)

# Serveur
PORT = 3002
HOST = '0.0.0.0'



# Route 1 : Acceuil 
# http://localhost:3002/
@app.route("/", methods=['GET'])
def home ():
   return make_response("<h1 style='color:blue'>Welcome to the Lieux service!</h1>", 200)

# Route 2 : GET les parks de la db
# http://localhost:3002/parks
@app.route("/parks", methods=["GET"])
def get_parks():
    parks = list(parks_collection.find({}, {"_id": 0}))
    return make_response(jsonify(parks), 200)

@app.route("/parks/len", methods=["GET"])
def get_len_parks():
    parks = list(parks_collection.find({}, {"_id": 0}))
    return jsonify({"count": len(parks)})


#Route 3: GET le park le plus proche du départ et l'arrivée
# http://localhost:3002/parks/nearest?start_lat=47.2184&start_lon=-1.5536&end_lat=47.2455&end_lon=-1.5584
@app.route("/parks/nearest", methods=["GET"])
def get_nearest_park():
    try:
        start_lat = float(request.args.get("start_lat"))
        start_lon = float(request.args.get("start_lon"))
        end_lat = float(request.args.get("end_lat"))
        end_lon = float(request.args.get("end_lon"))
    except (TypeError, ValueError):
        return make_response(jsonify({
            "error": "Invalid or missing coordinates"
        }), 400)

    parks = list(parks_collection.find({}, {"_id": 0}))

    nearest_park = None
    min_distance = float("inf")

    for park in parks:
        lat = float(park["latitude"])
        lon = float(park["longitude"])

        d1 = distance(start_lat, start_lon, lat, lon)
        d2 = distance(lat, lon, end_lat, end_lon)

        total_distance = d1 + d2

        if total_distance < min_distance:
            min_distance = total_distance
            nearest_park = park

    if nearest_park is None:
        return make_response(jsonify({
            "error": "No park found"
        }), 404)

    return make_response(jsonify({
        "park": nearest_park,
        "total_distance_km": round(min_distance, 2)
    }), 200)


## helper methods
def distance(lat1, lon1, lat2, lon2):
    # Distance à vol d'oiseau en kilomètres
    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (sin(dlat / 2) ** 2
         + cos(radians(lat1)) * cos(radians(lat2))
         * sin(dlon / 2) ** 2)

    return 2 * R * asin(sqrt(a))


# Lancement du serveur Flask
if __name__ == "__main__":
   
   if parks_collection.count_documents({}) == 0:
       init_parks()

   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
