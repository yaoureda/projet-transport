# IMPORTS DES PARCS NANTAIS DEPUIS UNE API VERS MONGO


# Imports 
import os
import requests
from pymongo import MongoClient
from enums import LocationType


# Url de l'API des parcs nantais
BASE_URL = "https://data.nantesmetropole.fr/api/explore/v2.1/catalog/datasets"

API_URL_PARKS = f"{BASE_URL}/244400404_parcs-jardins-nantes/records"
API_URL_TOILETS = f"{BASE_URL}/244400404_toilettes-publiques-nantes-metropole/records"


# Connexion à MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.environ["MONGO_DB"]]

parks_collection = db["parks"]
toilets_collection = db["toilets"]

COLLECTIONS = {
    LocationType.PARK: parks_collection,
    LocationType.TOILET: toilets_collection
}


# Récupération des lieux depuis l'API et stockage dans Mongo
def init_lieux(api_url, collection, extract_function):

    offset = 0
    limit = 100

    while True:
        response = requests.get(
            api_url,
            params={
                "limit": limit,
                "offset": offset
            },
            timeout=15
        )
        response.raise_for_status()

        data = response.json()
        lieux = data["results"]

        for lieu in lieux:
            document = extract_function(lieu)
            collection.insert_one(document)

        offset += len(lieux)

        if not lieux or offset >= data["total_count"]:
            break

    print(f"{collection.name} initialized successfully")


def extract_park(park):
    location = park["location"]

    return {
        "label": park.get("nom_complet"),
        "lat": location["lat"],
        "lon": location["lon"]
    }

def extract_toilet(toilet):
    lon, lat = toilet["geo_shape"]["geometry"]["coordinates"]

    return {
        "label": toilet.get("nom"),
        "lat": lat,
        "lon": lon
    }


def init_parks():
    init_lieux(API_URL_PARKS, parks_collection, extract_park)

def init_toilets():
    init_lieux(API_URL_TOILETS, toilets_collection, extract_toilet)