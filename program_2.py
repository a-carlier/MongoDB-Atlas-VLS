import pymongo
import time
import program_1 as p1
import database_info as dbi

worker = False  # Activate to make a worker out of the program
refresh_seconds = 60 * 2  # Refreshing Time in seconds


def init_static_stations(city):
    print("Init VLS Stations from " + city + " ...")
    client = pymongo.MongoClient(
        "mongodb+srv://" + dbi.db_user + ":" + dbi.db_password +
        "@cluster0.yxfmb.gcp.mongodb.net/" + dbi.db_name + "?retryWrites=true&w=majority")

    db = client.vls
    init_stations = p1.get_stations([city])

    for sta in init_stations:
        db.stations.update_one({
            "name": sta["name"]
        }, {
            "$set": sta
        }, upsert=True)  # Add the data if not found


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
    init_static_stations("paris")
    init_static_stations("lyon")
    init_static_stations("rennes")

    refresh("lille")
    refresh("paris")
    refresh("lyon")
    refresh("rennes")

    while True and worker:
        time.sleep(refresh_seconds)
        refresh("lille")
        refresh("paris")
        refresh("lyon")
        refresh("rennes")

