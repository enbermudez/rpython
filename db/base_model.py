class BaseModel:
    def __init__(self, name, db):
        self.name = name
        self.db = db
        self.collection = self.db[self.name]


    def insert_one(self, data):
        insert_id = self.collection.insert_one(data).inserted_id
        return insert_id


    def find_one(self, query):
        return self.collection.find_one(query)
