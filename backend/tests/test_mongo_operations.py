import unittest

from pymongo import MongoClient
from bson.objectid import ObjectId

from app.Pools import Pool
from app.Mongo import (
    create_pool,
    read_all_pools,
    retrieve_pool,
    update_pool,
    delete_pool,
    insert_pool_log,
    retrieve_pool_logs,
    delete_pool_logs,
    delete_all_pools,
    retrieve_pool_log_by_id,
    update_pool_log_by_id,
    delete_pool_log_by_id,
)

# Test MongoDB connection setup (use a test database)
TEST_MONGO_URI = "mongodb://user:password@localhost:27017/"
TEST_DB_NAME = "pool_database"
TEST_COLLECTION_NAME = "pool_collection"

client = MongoClient(TEST_MONGO_URI)
test_db = client[TEST_DB_NAME]
test_collection = test_db[TEST_COLLECTION_NAME]

# Mock database operations
pools_collection = test_collection  # Override the collection for testing


class TestMongoDBOperations(unittest.TestCase):
    def setUp(self):
        """
        Set up a clean test environment before each test.
        """
        pools_collection.delete_many({})  # Clear the test collection

    def tearDown(self):
        """
        Clean up after each test.
        """
        pools_collection.delete_many({})  # Clear the test collection

    def test_connection(self):
        """
        Test the MongoDB connection setup.
        """
        self.assertIsNotNone(client)
        self.assertIsNotNone(test_db)
        self.assertIsNotNone(test_collection)

    def test_create_pool(self):
        """
        Test inserting a new pool.
        """
        pool = Pool(
            owner_name="Alice",
            length=10.0,
            width=5.0,
            depth=2.0,
            type="chlorine",
            notes="Test pool",
        )
        pool_id = create_pool(pool)
        self.assertIsInstance(pool_id, str)

        retrieved_pool = pools_collection.find_one({"_id": ObjectId(pool_id)})
        self.assertIsNotNone(retrieved_pool)
        self.assertEqual(retrieved_pool["owner_name"], "Alice")

    def test_read_all_pools(self):
        """
        Test reading all pools from the database.
        """
        pool1 = Pool(owner_name="Bob", length=8, width=4, depth=1.5, type="salt")
        pool2 = Pool(owner_name="Jane", length=12, width=6, depth=2, type="chlorine")

        create_pool(pool1)
        create_pool(pool2)

        pools = read_all_pools()
        self.assertEqual(len(pools), 2)
        self.assertEqual(pools[0].owner_name, "Bob")
        self.assertEqual(pools[1].owner_name, "Jane")

    def test_retrieve_pool(self):
        """
        Test retrieving a specific pool by ID.
        """
        pool = Pool(owner_name="Eve", length=6, width=3, depth=1.8, type="salt")
        pool_id = create_pool(pool)

        retrieved_pool = retrieve_pool(pool_id)
        self.assertIsNotNone(retrieved_pool)
        self.assertEqual(retrieved_pool.owner_name, "Eve")

    def test_update_pool(self):
        """
        Test updating a pool's data.
        """
        pool = Pool(owner_name="John", length=10, width=4, depth=2, type="chlorine")
        pool_id = create_pool(pool)

        updated = update_pool(pool_id, {"notes": "Updated notes"})
        self.assertTrue(updated)

        updated_pool = pools_collection.find_one({"_id": ObjectId(pool_id)})
        self.assertEqual(updated_pool["notes"], "Updated notes")

    def test_delete_pool(self):
        """
        Test deleting a specific pool by ID.
        """
        pool = Pool(owner_name="Alice", length=10, width=5, depth=2, type="chlorine")
        pool_id = create_pool(pool)

        deleted = delete_pool(pool_id)
        self.assertTrue(deleted)

        retrieved_pool = pools_collection.find_one({"_id": ObjectId(pool_id)})
        self.assertIsNone(retrieved_pool)

    def test_pool_logs(self):
        """
        Test adding, retrieving, and deleting maintenance logs.
        """
        pool = Pool(owner_name="Charlie", length=9, width=4, depth=1.5, type="chlorine")
        pool_id = create_pool(pool)

        log_entry = {
            "id": "log1",
            "date": "2024-01-01",
            "pH_level": 7.5,
            "chlorine_level": 2.0,
            "notes": "Initial log",
        }
        log_added = insert_pool_log(pool_id, log_entry)
        self.assertTrue(log_added)

        logs = retrieve_pool_logs(pool_id)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["date"], "2024-01-01")

        logs_deleted = delete_pool_logs(pool_id)
        self.assertTrue(logs_deleted)

        logs = retrieve_pool_logs(pool_id)
        self.assertEqual(len(logs), 0)

    def test_delete_all_pools(self):
        """
        Test deleting all pools from the database.
        """
        pool1 = Pool(owner_name="Eve", length=6, width=3, depth=1.8, type="salt")
        pool2 = Pool(owner_name="Max", length=12, width=6, depth=2.5, type="chlorine")

        create_pool(pool1)
        create_pool(pool2)

        deleted_count = delete_all_pools()
        self.assertEqual(deleted_count, 2)

        pools = read_all_pools()
        self.assertEqual(len(pools), 0)

    def test_retrieve_pool_log_by_id(self):
        """
        Test retrieving a specific maintenance log by ID.
        """
        pool = Pool(owner_name="Diana", length=8, width=3, depth=2, type="chlorine")
        pool_id = create_pool(pool)

        log_entry = {
            "id": "log123",
            "date": "2024-01-02",
            "pH_level": 7.4,
            "chlorine_level": 2.5,
            "notes": "Routine check",
        }
        insert_pool_log(pool_id, log_entry)

        retrieved_log = retrieve_pool_log_by_id(pool_id, "log123")
        self.assertIsNotNone(retrieved_log)
        self.assertEqual(retrieved_log["id"], "log123")

    def test_update_pool_log_by_id(self):
        """
        Test updating a specific maintenance log by ID.
        """
        pool = Pool(owner_name="Edward", length=10, width=4, depth=2.5, type="salt")
        pool_id = create_pool(pool)

        log_entry = {
            "id": "log999",
            "date": "2024-01-03",
            "pH_level": 7.6,
            "chlorine_level": 1.8,
            "notes": "Initial maintenance",
        }
        insert_pool_log(pool_id, log_entry)

        updated_log = {
            "id": "log999",
            "date": "2024-01-03",
            "pH_level": 7.2,
            "chlorine_level": 2.0,
            "notes": "Updated maintenance log",
        }
        update_result = update_pool_log_by_id(pool_id, "log999", updated_log)
        self.assertTrue(update_result)

        logs = retrieve_pool_logs(pool_id)
        self.assertEqual(logs[0]["pH_level"], 7.2)
        self.assertEqual(logs[0]["notes"], "Updated maintenance log")

    def test_delete_pool_log_by_id(self):
        """
        Test deleting a specific maintenance log by ID.
        """
        pool = Pool(owner_name="Fiona", length=7, width=3.5, depth=2, type="chlorine")
        pool_id = create_pool(pool)

        log_entry = {
            "id": "log456",
            "date": "2024-01-04",
            "pH_level": 7.8,
            "chlorine_level": 1.5,
            "notes": "Weekly cleaning",
        }
        insert_pool_log(pool_id, log_entry)

        delete_result = delete_pool_log_by_id(pool_id, "log456")
        self.assertTrue(delete_result)

        logs = retrieve_pool_logs(pool_id)
        self.assertEqual(len(logs), 0)


if __name__ == "__main__":
    unittest.main()
