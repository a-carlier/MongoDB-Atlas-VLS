import pymongo
import database_info as dbi

# WE HAVE TO MAKE SURE THAT GEOLOCALISATION IS A 2D INDEX

"""
User program: give available stations name next to the user lat, lon with last data (bikes and stand)

x is the longitude 
y is the latitude

distance is the distance in meters from this location where we need to search
"""

def get_near_stations(x, y, distance):  # Distance in meters
    client = pymongo.MongoClient(
        "mongodb+srv://" + dbi.db_user + ":" + dbi.db_password +
        "@cluster0.yxfmb.gcp.mongodb.net/" + dbi.db_name + "?retryWrites=true&w=majority")

    db = client.vls
    cursor = db.stations.find(
        {
            "geolocalisation": {
                "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [x, y]
                },
                "$minDistance": 0,
                "$maxDistance": distance
                }
            }
        }
    )

    results = []
    for res in cursor:
        results.append(res)
    return results

if __name__ == "__main__":
    print(get_near_stations(3.06119, 50.63126, 100))  # Metres