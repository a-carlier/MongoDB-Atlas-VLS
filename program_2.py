import pymongo
import program_1 as p1

db_name = "vls"
db_user = "dbuser"
db_password = "xxx"


def refresh(city):
    print("Refreshing VLS from " + city + " ...")
    client = pymongo.MongoClient(
        "mongodb+srv://" + db_user + ":" + db_password +
        "@cluster0.yxfmb.gcp.mongodb.net/" + db_name + "?retryWrites=true&w=majority")

    db = client.vls
    refresh_stations = p1.get_stations(city)

    for sta in refresh_stations:
        db.stations.update_one({
            "name": sta["name"]
        }, {
            "$set": sta
        }, upsert=True)  # Add the data if not found


if __name__ == "__main__":
    refresh("lille")
    refresh("paris")
    refresh("lyon")
    refresh("rennes")
