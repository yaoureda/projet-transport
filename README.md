## Projet transport - UE Microservices


# Service 2 : Lieux

Renvoie les coordonnées du départ, de l'arrivée et le lieu le plus proche du trajet (park ou toilet au choix).
API GraphQL : `POST http://lieux:3002/graphql` (depuis un conteneur) ou `http://localhost:3002/graphql` (Insomnia).



## Requêtes

- **`geocode(req)`** : nom de lieu ou adresse → `{label, lat, lon}`, ou `null` si introuvable. Source : API IGN, limitée à Nantes.

- **`geocode_arr_dep(start, end, type=None)`** : géocode le départ et l'arrivée en un appel → `{start, end}`.
  
  Option : `nearest_location`, le parc qui rallonge le moins le trajet départ → lieu → arrivée.
  
  Il faut mentionner le type de lieu (PARK ou TOILET) si l'on veut `nearest_location`

- **`get_locations(type)`** : liste de tous les lieux de type `type` de Nantes → `[{label, lat, lon}]`. Source : open data Nantes Métropole, stockée dans MongoDB.

- **`get_nearest_location(type, start_lat, start_lon, end_lat, end_lon)`** : même calcul que `nearest_location`, mais à partir de coordonnées → `{location, total_distance_km}` (distance à vol d'oiseau).



## Exemple de requête principale 
```graphql
query { geocode_arr_dep(start: "gare de nantes", end: "imt atlantique", type: TOILET) { start { label lat lon } end { label lat lon } nearest_location { location { label lat lon } total_distance_km } } }
```
Lieu introuvable → `null`.