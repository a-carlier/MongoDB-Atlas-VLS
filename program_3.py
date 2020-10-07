import pymongo
import database_info as dbi

# WE HAVE TO MAKE SURE THAT GEOLOCATION IS A 2D INDEX

def get_near_stations(x, y, distance):  # Distance in meters
    client = pymongo.MongoClient(
        "mongodb+srv://" + dbi.db_user + ":" + dbi.db_password +
        "@cluster0.yxfmb.gcp.mongodb.net/" + dbi.db_name + "?retryWrites=true&w=majority")

    db = client.vls
    cursor = db.stations.find(
        {"geolocation": {
            "$near": [x, y],
            "$minDistance": 0,
            "$maxDistance": distance
        }}
    )

    results = []
    for res in cursor:
        results.append(res)
    return results

if __name__ == "__main__":
    print(get_near_stations(50.63126, 3.06119, 0.001))  # Radians