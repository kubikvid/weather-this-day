#  Copyright (c) 2019. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
from datetime import datetime

import pymongo

MONGO_HANDLER = pymongo.MongoClient('localhost')


class MongoHandler():
    def __init__(self):
        self.conn = MONGO_HANDLER
        self.db = self.conn.get_database('weather')

    def get_history(self, city_id: int, date: datetime, years=()):
        collection = self.db['history']

        date_match = {
            "$and": [
                {"month": date.month},
                {"day": date.day}
            ]
        }
        if years:
            date_match.get("$and").append({"year": {"$in": list(years)}})

        pipeline = [
            {"$match": {"city_id": city_id}},
            {"$project": {
                "_id": 0,
                "month": {"$month": "$date"},
                "year": {"$year": "$date"},
                "day": {"$dayOfMonth": "$date"},
                "temperature": 1
            }},
            {"$sort": {"year": 1}},
            {"$match": date_match}
        ]

        aggregation_result = collection.aggregate(pipeline)
        return list(aggregation_result)
