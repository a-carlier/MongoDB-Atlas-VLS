import pymongo
import database_info as dbi
import time
import re

# For this part, we only use data from Lille, so our history will have only one format
regex = re.compile("[0-9]{2}:([0-9]{2}):[0-9]{2}")
def is_time_correct(timest, h1, h2):
    val = time.gmtime(timest)
    if val.tm_wday > 4: # 0 to 4 are Monday to Friday
        return False

    if val.tm_hour > h1 and val.tm_hour < h2:
        return True
    return False


def get_stations_below_ratio(hour1 = 18, hour2 = 19, ratio=0.2):
    client = pymongo.MongoClient(
        "mongodb+srv://" + dbi.db_user + ":" + dbi.db_password +
        "@cluster0.yxfmb.gcp.mongodb.net/" + dbi.db_name + "?retryWrites=true&w=majority")

    db = client.vls

    s_list = db.stations.aggregate([
        {
            '$lookup': {
                'from': 'history',
                'let': {
                    "agg_id": "$aggregationid",  # FIELD WE CREATED IN PROGRAM 2
                    "total_velos": "$size"
                },
                'pipeline': [
                    {
                        '$match': {  # Jointure
                            '$expr': {'$eq': ['$aggregationid', '$$agg_id']}  # Joint stations with history
                        }
                    }, {  # Calculate ratio, day of week and hour
                        '$project': {
                            'week_day': {
                                '$dayOfWeek': '$datetime'
                            },
                            'hour': {
                                '$hour': '$datetime'
                            },
                            'ratio': {
                                '$cond': {
                                    'if': {'$eq': [{'$sum': ['$nbvelosdispo', '$nbplacesdispo']}, 0]},  # Some stations have a size of 0, still low ratio but we dont want to divide by 0
                                    'then': 0.0,
                                    'else': {'$divide': ['$nbvelosdispo', {'$sum': ['$nbvelosdispo', '$nbplacesdispo']}]}
                                }
                            }
                        }
                    }, {  # Ratio, day and hour match
                        '$match': {
                            'ratio': {'$lte': ratio},  # Match history with bikes ratio less than "ratio"
                            '$expr': {
                                '$and': [
                                    {'$gt': ['$week_day', 1]},  # After Sunday
                                    {'$lt': ['$week_day', 7]},  # Before Saturday
                                    {'$gt': ['$hour', hour1]},  # After hour1
                                    {'$lt': ['$hour', hour2]}  # Before hour2
                                ]
                            }
                        }
                    }
                ],
                'as': 'history'
            }
        }, {
            '$match': {
                'history': {'$not': {'$size': 0}}  # Filter out every stations for which previous history statements are false
            }
        }, {
            '$project': {
                'history': 0  # Delete history from result
            }
        }
    ])

    return s_list


if __name__ == "__main__":
    cursor = get_stations_below_ratio(20, 24, 0.2)

    i = 0
    for s in cursor:
        print(s)
        i += 1
    print(str(i) + " Stations")