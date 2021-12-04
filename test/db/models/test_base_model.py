import mongomock
import pymongo
import pytest
from pymongo.cursor import Cursor
from bson.objectid import ObjectId
from db.models.base_model import BaseModel

@mongomock.patch(servers = (('localhost')))
def test_insert_one():
    client = pymongo.MongoClient('localhost')
    basemodel = BaseModel("baselmodel", db = client.db)
    record_id = basemodel.insert_one({ "name": "John Doe" })

    assert isinstance(record_id, ObjectId)


@mongomock.patch(servers = (('localhost')))
def test_insert_many():
    client = pymongo.MongoClient('localhost')
    basemodel = BaseModel("baselmodel", db = client.db)
    records_ids = basemodel.insert_many([{ "name": "John Doe" }, { "name": "Mary Sue" }])

    assert len(records_ids) == 2


@mongomock.patch(servers = (('localhost')))
def test_find_one():
    client = pymongo.MongoClient('localhost')
    basemodel = BaseModel("baselmodel", db = client.db)
    record_id = basemodel.insert_one({ "name": "John Doe" })
    record_by_field = basemodel.find_one({ "name": "John Doe" })
    record_by_id = basemodel.find_one(record_id)

    assert record_by_field["_id"] == record_id
    assert record_by_id["_id"] == record_id


@mongomock.patch(servers = (('localhost')))
def test_find():
    client = pymongo.MongoClient('localhost')
    basemodel = BaseModel("baselmodel", db = client.db)
    basemodel.insert_many([{ "name": "John Doe" }, { "name": "John Doe" }, { "name": "Mary Sue" }])
    records_john = basemodel.find({ "name": "John Doe" })
    records_mary = basemodel.find({ "name": "Mary Sue" })

    assert records_john[0]["name"] == "John Doe"
    assert records_john[1]["name"] == "John Doe"
    with pytest.raises(IndexError):
        records_john[2]

    assert records_mary[0]["name"] == "Mary Sue"
    with  pytest.raises(IndexError):
        records_mary[1]


@mongomock.patch(servers = (('localhost')))
def test_update_one():
    client = pymongo.MongoClient('localhost')
    basemodel = BaseModel("baselmodel", db = client.db)
    record_id = basemodel.insert_one({ "name": "John Doe" })
    basemodel.update_one({ "_id": record_id }, { "name": "Mary Sue" })
    updated_record = basemodel.find_one({ "name": "Mary Sue" })

    assert updated_record["name"] == "Mary Sue"
    assert updated_record["_id"] == record_id


@mongomock.patch(servers = (('localhost')))
def test_update_many():
    client = pymongo.MongoClient('localhost')
    basemodel = BaseModel("baselmodel", db = client.db)
    basemodel.insert_many([{ "name": "John Doe" }, { "name": "John Doe" }, { "name": "Mary Sue" }])
    result = basemodel.update_many({ "name": "John Doe" }, { "name": "Mary Sue" })

    assert result.matched_count == 2
