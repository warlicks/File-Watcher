import unittest
import sqlite3
from filewatch import file_database  # Adjust this import to match your file name
import time


class TestFileWatcherDatabase(unittest.TestCase):
    def setUp(self):
        """Set up an in-memory database before each test"""
        self.db = FileWatcherDatabase(database_directory=":memory:")
        self.db.create_database_connection()
        self.db.create_table()

    def tearDown(self):
        """Close the database connection after each test"""
        if self.db.conn:
            self.db.conn.close()

    def test_database_connection(self):
        """Test if the database connection is established"""
        self.assertIsNotNone(self.db.conn)

    def test_create_table(self):
        """Test if the table is created successfully"""
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='file_events';")
        table = cursor.fetchone()
        self.assertIsNotNone(table)

    def test_insert_data(self):
        """Test inserting a row into the database"""
        event_time = int(time.time())
        self.db.insert_data(event_time, "created", "/path/to/file.txt", "txt", "/backup/file.txt")

        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM file_events;")
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], event_time)
        self.assertEqual(rows[0][2], "created")

    def test_query_by_file_extension(self):
        """Test querying by file extension"""
        self.db.insert_data(int(time.time()), "created", "/path/to/file.txt", "txt", None)
        self.db.insert_data(int(time.time()), "modified", "/path/to/file.py", "py", None)

        results = self.db.query_by_file_extension("txt")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][3], "txt")

    def test_query_by_event_type(self):
        """Test querying by event type"""
        self.db.insert_data(int(time.time()), "created", "/path/to/file.txt", "txt", None)
        self.db.insert_data(int(time.time()), "deleted", "/path/to/file2.txt", "txt", None)

        results = self.db.query_by_event_type("deleted")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][2], "deleted")

    def test_query_by_event_location(self):
        """Test querying by event location"""
        self.db.insert_data(int(time.time()), "created", "/home/user/documents/file1.txt", "txt", None)
        self.db.insert_data(int(time.time()), "created", "/home/user/downloads/file2.txt", "txt", None)

        results = self.db.query_by_event_location("/home/user/documents")
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0][3].startswith("/home/user/documents"))

    def test_query_by_event_date(self):
        """Test querying by date range"""
        now = int(time.time())
        past = now - 1000
        future = now + 1000

        self.db.insert_data(past, "created", "/path/to/file1.txt", "txt", None)
        self.db.insert_data(now, "modified", "/path/to/file2.txt", "py", None)

        results = self.db.query_by_event_date(past, future)
        self.assertEqual(len(results), 2)

    def test_error_handling(self):
        """Test handling of incorrect SQL execution"""
        with self.assertRaises(sqlite3.Error):
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT * FROM non_existing_table;")

if __name__ == "__main__":
    unittest.main()
