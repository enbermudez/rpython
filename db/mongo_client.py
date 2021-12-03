from pymongo import MongoClient
import json

class DBClient:
    def __init__(self, database, env):
        self.get_connection_params()
        self.client = MongoClient(self.host, self.port)
        self.db = self.client[f"{database}-{env}"]

    def get_connection_params(self):
        file = open("db/config.json", "r")
        data = json.load(file)

        self.host = data["host"]
        self.port = data["port"]

        file.close()
