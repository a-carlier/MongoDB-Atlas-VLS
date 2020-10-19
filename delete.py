import pymongo
import database_info as dbi

def del_stations(station_name):
    client = pymongo.MongoClient(
        "mongodb+srv://" + dbi.db_user + ":" + dbi.db_password +
        "@cluster0.yxfmb.gcp.mongodb.net/" + dbi.db_name + "?retryWrites=true&w=majority")

    stations = client.vls.stations
    my_station=(stations.find_one_and_delete({'name':station_name}))
    if(my_station):
        aggreg=my_station['aggregationid']
        client.vls.history.delete_many({'aggregationid':aggreg})

if __name__ == "__main__":

    print(del_stations("OPERA"))