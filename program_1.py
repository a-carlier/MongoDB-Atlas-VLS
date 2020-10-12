import requests
import json
import time

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

def get_stations(cities=["lille", "paris", "lyon", "rennes"], live_data=False):

    stations = []

    if "lille" in cities:
        # At writing time, there is 251 stations, 300 rows will be sufficent
        url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=300"
        response = requests.request("GET", url)
        response_json = json.loads(response.text.encode('utf8'))

        records = response_json.get("records", [])
        
        for element in records:

            if live_data:
                element['fields']['timestamp'] = time.time()
                element['fields']['aggregationid'] = 59000000 + element['fields']['libelle']  # 59000000 for Lille
                stations.append(element['fields'])

                continue

            new_el = {
                'geometry': element['geometry'],
                'size': element['fields']['nbvelosdispo'] + element['fields']['nbplacesdispo'],
                'name': element['fields']['nom'],
                'tpe': True if element['fields']['type'] == 'AVEC TPE' else False,
                'available': True if element['fields']['etat'] == 'EN SERVICE' else False,
                'aggregationid': 59000000 + element['fields']['libelle']
            }

            stations.append(new_el)

    if "paris" in cities:
        url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=1500"
        response = requests.request("GET", url)
        response_json = json.loads(response.text.encode('utf8'))

        records = response_json.get("records", [])

        for element in records:

            if live_data:
                element['fields']['timestamp'] = time.time()
                element['fields']['aggregationid'] = 75000000 + int(element['fields']['stationcode'])  # 75000000 for Lille
                stations.append(element['fields'])
                continue

            new_el = {
                'geometry': element['geometry'],
                'size': element['fields']['capacity'],
                'name': element['fields']['name'],
                'tpe': True if element['fields']['is_renting'] == 'OUI' else False,
                'available': True if element['fields']['is_installed'] == 'OUI' else False,
                'aggregationid': 75000000 + int(element['fields']['stationcode'])
            }

            stations.append(new_el)

    if "lyon" in cities:
        url = "https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json?maxfeatures=500&start=1"
        response = requests.request("GET", url)
        response_json = json.loads(response.text.encode('utf8'))

        records = response_json.get("values", [])

        for element in records:

            if live_data:
                element['timestamp'] = time.time()
                element['aggregationid'] = 69000000 + element['number']  # 69000000 for Lyon
                stations.append(element)
                continue

            new_el = {
                'geometry': {
                    "type": "Point",
                    "coordinates": [
                        element['lng'],
                        element['lat']
                    ]
                },
                'size': element['bike_stands'],
                'name': element['name'],
                'tpe': element['banking'],
                'available': True if element['availabilitycode'] == 1 else False,
                'aggregationid': 69000000 + element['number']
            }

            stations.append(new_el)

    if "rennes" in cities:
        # At writing time, there is 99 stations, 100 rows will be sufficent
        url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=stations_vls&q=&rows=100"
        response = requests.request("GET", url)
        response_json = json.loads(response.text.encode('utf8'))

        records = response_json.get("records", [])

        for element in records:

            if live_data:
                element['fields']['timestamp'] = time.time()
                element['fields']['aggregationid'] = 35000000 + element['fields']['objectid']  # 35000000 for Rennes
                stations.append(element['fields'])
                continue

            new_el = {
                'geometry': element['geometry'],
                'size': element['fields']['nb_socles'],
                'name': element['fields']['nom'],
                'tpe': True if element['fields']['tpe'] == 'oui' else False,
                'available': True if element['fields']['etat'] == 'Ouverte' else False,
                'aggregationid': 35000000 + element['fields']['objectid']  # 35000000 for Rennes
            }

            stations.append(new_el)

    return stations

if __name__ == "__main__":
    print(get_stations())