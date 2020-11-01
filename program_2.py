import pymongo
import time
import program_1 as p1
import database_info as dbi

worker = True  # Activate to make a worker out of the program
refresh_seconds = 60 * 2  # Refreshing Time in seconds

"""
Worker who refresh and store live data for a city (history data)

We also use init_static_stations on start to make sure they are in the database and update them with live information
stations will be our Database with stations
history will be our Database with history

They can be aggregated with their aggregationid
"""

def init_static_stations(city):
    print("Init VLS Stations from " + city + " ...")
    client = pymongo.MongoClient(
        "mongodb+srv://" + dbi.db_user + ":" + dbi.db_password +
        "@cluster0.yxfmb.gcp.mongodb.net/" + dbi.db_name + "?retryWrites=true&w=majority")

    db = client.vls
    init_stations = p1.get_stations([city])

    for sta in init_stations:
        # It's important not using update Many, because we don't want to overwrite everything, some stations are
        # updated, some are added
        db.stations.update_one({
            "aggregationid": sta["aggregationid"]
        }, {
            "$set": sta
        }, upsert=True)  # Add the data if not found

    db.stations.create_index([("geolocalisation", "2dsphere")])
    db.stations.create_index([("aggregationid", 1)])


def refresh(city):
    print("Refreshing VLS from " + city + " ...")
    client = pymongo.MongoClient(
        "mongodb+srv://" + dbi.db_user + ":" + dbi.db_password +
        "@cluster0.yxfmb.gcp.mongodb.net/" + dbi.db_name + "?retryWrites=true&w=majority")

    db = client.vls
    refresh_stations = p1.get_stations([city], True)

    db.history.insert_many(refresh_stations)
    # USE HISTORY COLLECTION # MORE DATA BECAUSE OF TIMESTAMP DIFFERENCE


if __name__ == "__main__":
    init_static_stations("lille")
    # init_static_stations("paris")
    # init_static_stations("lyon")
    # init_static_stations("rennes")

    refresh("lille")
    # refresh("paris")
    # refresh("lyon")
    # refresh("rennes")

    while True and worker:
        print("Waiting " + str(refresh_seconds) + " seconds before next refresh...")
        time.sleep(refresh_seconds)
        refresh("lille")
        # refresh("paris")
        # refresh("lyon")
        # refresh("rennes")

