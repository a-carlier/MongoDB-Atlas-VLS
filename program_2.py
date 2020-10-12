import pymongo
import program_1 as p1
import database_info as dbi


def refresh(city):
    print("Refreshing VLS from " + city + " ...")
    client = pymongo.MongoClient(
        "mongodb+srv://" + dbi.db_user + ":" + dbi.db_password +
        "@cluster0.yxfmb.gcp.mongodb.net/" + dbi.db_name + "?retryWrites=true&w=majority")

    db = client.vls
    refresh_stations = p1.get_stations(city)

    for sta in refresh_stations:
        db.stations.update_one({
            "name": sta["name"],
            "timestamp": sta["timestamp"]
        }, {
            "$set": sta
        }, upsert=True)  # Add the data if not found


if __name__ == "__main__":
    refresh("lille")
    refresh("paris")
    refresh("lyon")
    refresh("rennes")

    """
    while True:
        time.sleep(60 * 1000)
        refresh("lille")
        refresh("paris")
        refresh("lyon")
        refresh("rennes")
    """
