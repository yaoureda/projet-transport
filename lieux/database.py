
import os
import requests
from pymongo import MongoClient, UpdateOne, GEOSPHERE

API_URL = (
    "https://data.nantesmetropole.fr/api/explore/v2.1/"
    "catalog/datasets/244400404_parcs-jardins-nantes/records"
)

# Connexion à MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["places_db"]
parks_collection = db["parks"]


def init_parks():

    offset = 0
    limit = 100

    while True:
        response = requests.get(
            API_URL,
            params={
                "select": "nom_complet,longitude,latitude",
                "limit": limit,
                "offset": offset
            },
            timeout=15
        )
        response.raise_for_status()

        data = response.json()
        records = data["results"]

        for park in records:

            document = {
                "nom": park.get("nom_complet"),
                "latitude": park.get("latitude"),
                "longitude": park.get("longitude"),
            }

            parks_collection.insert_one(document)

        offset += len(records)

        if not records or offset >= data["total_count"]:
            break

    print("Parks initialized successfully")


if __name__ == "__main__":
    init_parks()
