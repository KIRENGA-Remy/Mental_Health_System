import pymongo
url='mongodb://localhost:27017/mental_health_system'
client = pymongo.MongoClient(url)
db=client['mental_health_system']
