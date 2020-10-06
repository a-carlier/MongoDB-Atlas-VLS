import requests
import json

"""
Objectif: Récuperer les donnees suivantes des APIS de Velib de Lille, Paris, Lyon et Rennes
- geolocation
- name
- capacity
- tpe
- available

Nous retransformons les fichiers pour obtenir des resultats coherents avec les memes types
de valeurs et memes cles

"""

def get_stations(cities=["lille", "paris", "lyon", "rennes"]):

    stations = []

    if "lille" in cities:
        # At writing time, there is 251 stations, 300 rows will be sufficent
        url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=300"
        response = requests.request("GET", url)
        response_json = json.loads(response.text.encode('utf8'))

        records = response_json.get("records", [])
        
        for element in records:
            element['fields'].pop('etatconnexion', None)
            element['fields'].pop('commune', None)
            element['fields'].pop('libelle', None)
            element['fields'].pop('datemiseajour', None)
            element['fields'].pop('localisation', None)
            element['fields'].pop('adresse', None)

            element['fields']['geolocation'] = element['fields']['geo']
            element['fields'].pop('geo', None)
            element['fields']['size'] = element['fields']['nbvelosdispo'] + element['fields']['nbplacesdispo']
            element['fields'].pop('nbplacesdispo', None)
            element['fields'].pop('nbvelosdispo', None)
            element['fields']['name'] = element['fields']['nom']
            element['fields'].pop('nom', None)
            element['fields']['tpe'] = True if element['fields']['type'] == 'AVEC TPE' else False
            element['fields'].pop('type', None)
            element['fields']['available'] = True if element['fields']['etat'] == 'EN SERVICE' else False
            element['fields'].pop('etat', None)

            stations.append(element['fields'])

    if "paris" in cities:
        url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=1500"
        response = requests.request("GET", url)
        response_json = json.loads(response.text.encode('utf8'))

        records = response_json.get("records", [])

        for element in records:
            element['fields'].pop('ebike', None)
            element['fields'].pop('nom_arrondissement_communes', None)
            element['fields'].pop('numbikesavailable', None)
            element['fields'].pop('mechanical', None)
            element['fields'].pop('stationcode', None)
            element['fields'].pop('numdocksavailable', None)
            element['fields'].pop('duedate', None)
            element['fields'].pop('is_returning', None)

            element['fields']['geolocation'] = element['fields']['coordonnees_geo']
            element['fields'].pop('coordonnees_geo', None)
            element['fields']['size'] = element['fields']['capacity']
            element['fields'].pop('capacity', None)
            # element['fields']['name'] = element['fields']['name']
            # element['fields'].pop('name', None)
            element['fields']['tpe'] = True if element['fields']['is_renting'] == 'OUI' else False
            element['fields'].pop('is_renting', None)
            element['fields']['available'] = True if element['fields']['is_installed'] == 'OUI' else False
            element['fields'].pop('is_installed', None)

            stations.append(element['fields'])

    if "lyon" in cities:
        url = "https://transport.data.gouv.fr/gbfs/lyon/station_information.json"
        response = requests.request("GET", url)
        response_json = json.loads(response.text.encode('utf8'))

        records = response_json.get("data", {})["stations"]

        for element in records:
            element.pop('station_id', None)
            element.pop('address', None)

            element['geolocation'] = [element['lat'], element['lon']]
            element.pop('lat', None)
            element.pop('lon', None)
            element['size'] = element['capacity']
            element.pop('capacity', None)
            # element['fields']['name'] = element['fields']['nom']
            # element['fields'].pop('nom', None)
            element['tpe'] = False # Unknown
            element['available'] = False # Unknown

            stations.append(element)

    if "rennes" in cities:
        # At writing time, there is 99 stations, 100 rows will be sufficent
        url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=stations_vls&q=&rows=100"
        response = requests.request("GET", url)
        response_json = json.loads(response.text.encode('utf8'))

        records = response_json.get("records", [])

        for element in records:
            element['fields'].pop('x_cc48', None)
            element['fields'].pop('metro', None)
            element['fields'].pop('objectid', None)
            element['fields'].pop('d_mhs', None)
            element['fields'].pop('code_exploitation', None)
            element['fields'].pop('adresse', None)
            element['fields'].pop('d_mes', None)
            element['fields'].pop('y_cc48', None)
            element['fields'].pop('vls_id', None)
            element['fields'].pop('geo_shape', None)

            element['fields']['geolocation'] = element['fields']['geo_point_2d']
            element['fields'].pop('geo_point_2d', None)
            element['fields']['size'] = element['fields']['nb_socles']
            element['fields'].pop('nb_socles', None)
            element['fields']['name'] = element['fields']['nom']
            element['fields'].pop('nom', None)
            element['fields']['tpe'] = True if element['fields']['tpe'] == 'oui' else False
            # element['fields'].pop('type', None)
            element['fields']['available'] = True if element['fields']['etat'] == 'Ouverte' else False
            element['fields'].pop('etat', None)

            stations.append(element['fields'])

    return stations

if __name__ == "__main__":
    print(get_stations())