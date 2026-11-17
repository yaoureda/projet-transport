## Projet transport - UE Microservices


# Service 2 : Lieux

Renvoie les coordonnées du départ, de l'arrivée et du parc le plus proche du trajet.
API GraphQL : `POST http://lieux:3002/graphql` (depuis un conteneur) ou `http://localhost:3002/graphql` (Insomnia).



## Requêtes

- **`geocode(req)`** : nom de lieu ou adresse → `{label, lat, lon}`, ou `null` si introuvable. Source : API IGN, limitée à Nantes.

- **`geocode_arr_dep(start, end)`** : géocode le départ et l'arrivée en un appel → `{start, end}`.
  Option : `nearest_park`, le parc qui rallonge le moins le trajet départ → parc → arrivée.

- **`get_parks`** : liste de tous les parcs de Nantes → `[{label, lat, lon}]`. Source : open data Nantes Métropole, stockée dans MongoDB.

- **`get_nearest_park(start_lat, start_lon, end_lat, end_lon)`** : même calcul que `nearest_park`, mais à partir de coordonnées → `{location, total_distance_km}` (distance à vol d'oiseau).



## Exemple de requête principale 
```graphql
query { geocode_arr_dep(start: "gare de nantes", end: "imt atlantique") { start { lat lon } end { lat lon } nearest_park { location { label lat lon } total_distance_km } } }
```
Lieu introuvable → `null`.