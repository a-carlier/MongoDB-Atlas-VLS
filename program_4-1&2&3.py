import re  # REGEX
import pymongo
import database_info as dbi

# PROGRAM OBJECTIVES:
# - find station with name (with some letters)
#   * Find a station with a word(s) case insensitive
# - update a station
# - delete a station

def find_station_name(name):
    # STATION REGEX FINDING
    client = pymongo.MongoClient(
        "mongodb+srv://" + dbi.db_user + ":" + dbi.db_password +
        "@cluster0.yxfmb.gcp.mongodb.net/" + dbi.db_name + "?retryWrites=true&w=majority")

    regex = re.compile(".*" + name + ".*", re.IGNORECASE)

    db = client.vls
    cursor = db.stations.find({
        "name": {"$regex": regex}
    })

    results = []
    for res in cursor:
        results.append(res)
    return results


def value_update(stationu):
    # UPDATING INTERFACE (Not sending to database)
    print("Which value do you want to change from station " + stationu["name"] + "?")
    print("- name: " + str(stationu["name"]))
    print("- size: " + str(stationu["size"]))
    print("- available: " + str(stationu["available"]))
    print("- tpe: " + str(stationu["tpe"]))
    print("- geolocalisation: " + "lat: " + str(stationu["geolocalisation"]["coordinates"][1]) + ", lon: " + str(stationu["geolocalisation"]["coordinates"][0]))

    idu = input("Value to update: ")

    while True:
        if idu != "name" and idu != "size" and idu != "available" and idu != "tpe" and idu != "geolocalisation":
            print("Value is not correct, please try again: ")
            idu = input("Value to update: ")
            continue
        break

    if idu == "name":
        print("Please prompt a new Name for " + stationu["name"])
        valin = input("name: ")
        stationu["name"] = valin

    elif idu == "size":
        print("Please prompt a new Size for " + stationu["name"])
        valin = input("size (integer): ")

        while True:
            try:
                temp = int(valin)
                break  # Successful int
            except:
                print("Size incorrect, please try again: ")
                valin = input("size (integer): ")
        stationu["size"] = int(valin)

    elif idu == "available":
        print("Please prompt a new Availability for " + stationu["name"])
        valin = input("available (TRUE/FALSE): ")

        while True:
            if valin != "TRUE" and valin != "FALSE":
                print("Availability incorrect, please try again: ")
                valin = input("available (TRUE/FALSE): ")
                continue
            break  # Else
        stationu["available"] = True if valin == "TRUE" else False

    elif idu == "tpe":
        print("Please prompt a new TPE for " + stationu["name"])
        valin = input("tpe (TRUE/FALSE): ")

        while True:
            if valin != "TRUE" and valin != "FALSE":
                print("TPE incorrect, please try again: ")
                valin = input("tpe (TRUE/FALSE): ")
                continue
            break  # Else
        stationu["tpe"] = True if valin == "TRUE" else False

    elif idu == "geolocalisation":
        print("Please prompt a new Latitude for " + stationu["name"])
        valin = input("latitude (float): ")

        while True:
            try:
                temp = float(valin)
                break  # Successful float
            except:
                print("Latitude incorrect, please try again: ")
                valin = input("latitude (float): ")

        stationu["geolocalisation"]["coordinates"][1] = float(valin)

        print("Please prompt a new Longitude for " + stationu["name"])
        valin = input("longitude (float): ")

        while True:
            try:
                temp = float(valin)
                break  # Successful float
            except:
                print("Longitude incorrect, please try again: ")
                valin = input("longitude (float): ")

        stationu["geolocalisation"]["coordinates"][0] = float(valin)

    return stationu


def which_station(results):
    # INTERFACE CHOOSING STATION AND UPDATING OR DELETING THIS STATION
    print("Please prompt which station you want to update by entering its ID: ")
    idu = input("ID to update: ")

    while True:
        try:
            if int(idu) < 0 or int(idu) > len(results):
                print("ID is not correct, please try again: ")
                idu = input("ID to update: ")
                continue
            break
        except:
            idu = -1  # Fail, user prompt a string

    stationu = results[int(idu)-1]

    client = pymongo.MongoClient(
        "mongodb+srv://" + dbi.db_user + ":" + dbi.db_password +
        "@cluster0.yxfmb.gcp.mongodb.net/" + dbi.db_name + "?retryWrites=true&w=majority")

    db = client.vls

    print("Do you want to UPDATE or DELETE this station?")
    valin = input("(UPDATE/DELETE): ")

    while True:
        if valin != "UPDATE" and valin != "DELETE":
            print("Prompt incorrect, please try again: ")
            valin = input("(UPDATE/DELETE): ")
            continue
        break  # Else

    if valin == "DELETE":
        delete_station(stationu)
    elif valin == "UPDATE":
        while True:
            stationu = value_update(stationu)

            print("Updating Database...")
            db.stations.update_one({
                "aggregationid": stationu["aggregationid"]
            }, {
                "$set": stationu
            }, upsert=True)  # Add the data if not found

            print("Would you like to change another value?")
            valin = input("(Y/N): ")

            while True:
                if valin != "Y" and valin != "N":
                    valin = input("(Y/N): ")
                    continue
                break  # Else

            if valin == "N":
                break
            # Else, continue...


def delete_station(station):
    # DELETE STATION FROM DATABASE AND HISTORY
    client = pymongo.MongoClient(
        "mongodb+srv://" + dbi.db_user + ":" + dbi.db_password +
        "@cluster0.yxfmb.gcp.mongodb.net/" + dbi.db_name + "?retryWrites=true&w=majority")

    stations = client.vls.stations
    my_station = stations.find_one_and_delete({'aggregationid': station["aggregationid"]})

    if (my_station):  # Check Deleted
        client.vls.history.delete_many({'aggregationid': station["aggregationid"]})

    print("Station and associated History deleted")


def main():
    print("Please prompt a name value to search in the database: ")
    name = input("Name prompt: ")

    results = find_station_name(name)

    i = 0
    for res in results:
        i += 1
        print("ID " + str(i) + ": " + res["name"])

    if len(results) < 1:
        print("No stations Found")
        return 0

    which_station(results)


if __name__ == "__main__":
    main()