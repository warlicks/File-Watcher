import os
import sqlite3
from sqlite3 import Error
from typing import Union


class FileWatcherDatabase:
    def __init__(
        self, database_directory: str = ".", database_name: str = "file_watch.db"
    ) -> None:
        """Creates a FileWatcherDatabase instance

        _extended_summary_

        Args:
            database_directory (str, optional): The directory where the database
              is stored. Defaults to users home directory (~).
            database_name (str, optional): The name of the database file. Defaults
              to 'file_watch.db'.
        """
        self.__database_location = os.path.join(
            os.path.abspath(database_directory), database_name
        )
        self.__conn: Union[sqlite3.Connection, None] = None

    @property
    def conn(self):
        return self.__conn

    def create_database_connection(self):
        """Creates database connection

        If there is not a file at the database location a sqllite database
          is created at that location.
        """
        try:
            self._conn = sqlite3.connect(self.__database_location)
        except sqlite3.OperationalError as e:
            print(f"Failed to open {self.__database_location}")

    def create_table(self):
        """Creates table to hold file changes into the event."""
        try:
            c = self._conn.cursor()
            c.execute(self.__create_table_sql())
        except Error as e:
            print(e)

    def __insert_data_sql(self):
        """Inserts a new record into the file_events table """
        if self.__conn is None:
            print('Error: Database connection is not established')
            return

        try:
            c = self.__conn.cursor()
            c.execute(self.__insert_data_sql(), (event_id, event_time, event_type, event_location, file_type, move_destinatino))
            self.__conn.commit()
        except sqlite3.Error as e:
            print(f'Database error:{e}')

    def query_by_file_extension(self, ext_param: str):
        """Queries the database by file type.


        Args:
            ext_param (str): The file extension of interest.
        """
        c = self.__conn.cursor()
        c.execute(self.__file_extension_query(), (ext_param))

        rows = c.fetchall()
        # TODO: replace this place holder with how we actually display this data.
        for row in rows:
            print(row)

    def __create_table_sql(self) -> str:
        """Holds query string for creating table."""

        sql = """
        CREATE TABLE If NOt EXISTS file_events (
	      "event_id"	INTEGER NOT NULL,
	      "event_time"	INTEGER NOT NULL,
	      "event_type"	TEXT NOT NULL,
	      "event_location"	TEXT NOT NULL,
	      "file_type"	INTEGER,
	      "move destination"	TEXT,
	      PRIMARY KEY("event_id" AUTOINCREMENT)
        );
        """
        return sql

    def __file_extension_query(self) -> str:
        """returns SQL query for selecting by file extension"""
        return """
        
        SELECT
            *

        FROM  file_events

        Where
            file_type = ?

        """
