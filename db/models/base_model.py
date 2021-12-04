class BaseModel:
    def __init__(self, name, db):
        self.name = name
        self.db = db
        self.collection = self.db[self.name]


    def insert_one(self, data):
        inserted_id = self.collection.insert_one(data).inserted_id
        return inserted_id


    def insert_many(self, data):
        result = self.collection.insert_many(data)
        return result.inserted_ids


    def find_one(self, query):
        return self.collection.find_one(query)


    def find(self, query):
        return self.collection.find(query)


    def update_one(self, query, data):
        return self.collection.update_one(query, { "$set": data }, upsert = False)


    def update_many(self, query, data):
        return self.collection.update_many(query, { "$inc": data }, upsert = False)
