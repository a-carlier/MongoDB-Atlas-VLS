import pymongo
import database_info as dbi

def deactivate_area(points, type=False):
    if len(points) < 3:
        print("You need to give more points to deactivate an area")

    if points[0] != points[-1]:  # Closing loop in case it is open
        points.append(points[0])

    client = pymongo.MongoClient(
        "mongodb+srv://" + dbi.db_user + ":" + dbi.db_password +
        "@cluster0.yxfmb.gcp.mongodb.net/" + dbi.db_name + "?retryWrites=true&w=majority")

    db = client.vls

    db.stations.update_many({
        'geolocalisation': {
            "$geoWithin": {
                "$geometry": {
                    "type": "Polygon",
                    "coordinates": [points]  # Double Array of points
                }
            }
        }
    }, {
        '$set': {
            'available': type
        }
    })


if __name__ == "__main__":
    deactivate_area([
        [3.0568, 50.6347],
        [3.0717, 50.6332],
        [3.0686, 50.6238],
        [3.0424, 50.6287],  # We can except the closing Point because we are checking it
        [3.0568, 50.6347]   # Anyway, the closing point must be the same that the first point
    ], False)  # We can also omit False, but we could ACTIVATE all station by changing it to True