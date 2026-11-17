# GÉOCODAGE (CONVERTIR UN NOM EN COORDONNÉES VIA L'API IGN)


# Imports 
import requests                                            


# Variables globales 
GEOCODE_URL = "https://data.geopf.fr/geocodage/search"           # API géocodage IGN
NANTES_CITYCODE = "44109"                                        # limitation à la ville de Nantes 
TIMEOUT = 20                                                   # temps d'attente max avant réponse                                                     


# Fonction de géocodage 
def geocode(req):   

    # Réponse 
    response = requests.get(
        GEOCODE_URL, 
        params={"q": req, "index": "address,poi", "citycode": NANTES_CITYCODE}, # Poi permet de prendre en compte les leixu nommés
        timeout=TIMEOUT)  # Appel GET à l'API  

    # Résultats
    features = response.json()["features"] 

    # Si aucun résultat
    if not features:                                                
        return None
    lon, lat = features[0]["geometry"]["coordinates"] 
    props = features[0]["properties"] # Résultat le plus pertinent          
    return {"label": props.get("label") or props.get("toponym"), "lat": lat, "lon": lon} # Récupération du nom


# Fonction géocodage départ arrivée 
def geocode_arr_dep(start, end):                                       
    return {"start": geocode(start), "end": geocode(end)}           


# Test local
if __name__ == "__main__":                                         
    print(geocode("gare de nantes"))                                
    print(geocode("abcd"))                                         
    print(geocode_arr_dep("gare de nantes", "imt atlantique"))       