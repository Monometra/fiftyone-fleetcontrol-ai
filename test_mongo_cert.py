import pymongo
import certifi

uri = "mongodb+srv://dkarinamendezd_db_user:lCDnIRb0qQxcNDnw@cluster0.ux8amal.mongodb.net/?tlsCAFile=" + certifi.where()
try:
    client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
    print("Connected:", client.server_info()["version"])
except Exception as e:
    print("Error:", e)
