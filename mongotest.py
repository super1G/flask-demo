from pymongo import MongoClient

client = MongoClient("mongodb://localhost")

db = client.Test
db.user.insert_one({'name': 'user', 'passward': 'pass'}
                   )