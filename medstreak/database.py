from pymongo import MongoClient


def getDB():
    client = MongoClient(
    'mongodb://medstreak:medstreak@medstreak-dev-shard-00-00-8ghe7.mongodb.net:27017,medstreak-dev-shard-00-01-8ghe7.mongodb.net:27017,medstreak-dev-shard-00-02-8ghe7.mongodb.net:27017/medstreak-dev?ssl=true&replicaSet=MedStreak-Dev-shard-0&authSource=admin&retryWrites=true')
    return client['medstreak-dev']