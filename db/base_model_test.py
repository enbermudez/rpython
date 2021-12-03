import unittest
import mongomock
import pymongo
from pymongo.cursor import Cursor
from bson.objectid import ObjectId
from db.base_model import BaseModel

class TestBaseModel(unittest.TestCase):
    @mongomock.patch(servers = (('localhost')))
    def test_insert_one(self):
        client = pymongo.MongoClient('localhost')
        basemodel = BaseModel("baselmodel", db = client.db)
        record_id = basemodel.insert_one({ "name": "John Doe" })

        self.assertIsInstance(record_id, ObjectId)


    @mongomock.patch(servers = (('localhost')))
    def test_insert_many(self):
        client = pymongo.MongoClient('localhost')
        basemodel = BaseModel("baselmodel", db = client.db)
        records_ids = basemodel.insert_many([{ "name": "John Doe" }, { "name": "Mary Sue" }])

        self.assertEqual(len(records_ids), 2)


    @mongomock.patch(servers = (('localhost')))
    def test_find_one(self):
        client = pymongo.MongoClient('localhost')
        basemodel = BaseModel("baselmodel", db = client.db)
        record_id = basemodel.insert_one({ "name": "John Doe" })
        record_by_field = basemodel.find_one({ "name": "John Doe" })
        record_by_id = basemodel.find_one(record_id)

        self.assertEqual(record_by_field["_id"], record_id)
        self.assertEqual(record_by_id["_id"], record_id)


    @mongomock.patch(servers = (('localhost')))
    def test_find(self):
        client = pymongo.MongoClient('localhost')
        basemodel = BaseModel("baselmodel", db = client.db)
        record_id = basemodel.insert_many([{ "name": "John Doe" }, { "name": "John Doe" }, { "name": "Mary Sue" }])
        records_john = basemodel.find({ "name": "John Doe" })
        records_mary = basemodel.find({ "name": "Mary Sue" })

        self.assertEqual(records_john[0]["name"], "John Doe")
        self.assertEqual(records_john[1]["name"], "John Doe")
        with self.assertRaises(IndexError):
            records_john[2]

        self.assertEqual(records_mary[0]["name"], "Mary Sue")
        with self.assertRaises(IndexError):
            records_mary[1]
