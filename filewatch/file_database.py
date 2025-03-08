import os
import sqlite3
from sqlite3 import Error
from typing import Optional

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
        self.__conn: Optional[sqlite3.Connection, None] = None

    @property
    def conn(self):
        """Returns the connection to the database"""
        return self.__conn

    def create_database_connection(self):
        """Creates database connection
        If there is not a file at the database location a SQLite database
          is created at that location.
        """
        if self.__conn is None:
            try:
                self.__conn = sqlite3.connect(self.__database_location)
            except sqlite3.Error as e:
                raise ConnectionError(f"Failed to open {self.__database_location}: {e}")
            return self.__conn

    def create_table(self):
        """Creates table to hold file changes into the event."""
        query = self._create_table_sql()
        self._execute_query(query)

    def insert_data(
        self,
        event_time: int,
        event_type: str,
        event_location: str,
        file_type: str,
        move_destination: Optional[str] = None,
    ):
        """
        Inserts data into the database.

        Args:
            event_time (int): The time of the event. The time should already be converted to epoch
            event_type (str): The type of the event.
            event_location (str): The location of the event.
            file_type (str): The type of the file.
            move_destination (str, Optional): The destination where the file is moved. Defaults to None.
        Returns:
            None
        Raises:
            sqlite3.Error: If there is an error with the database operation.
        """
        query = self._insert_data_sql()
        params = (event_time, event_type, event_location, file_type, move_destination)
        self._execute_query(query, params)

    def query_by_file_extension(self, ext_param: str) -> list:
        """Queries the database by file type.
        Args:
            ext_param (str): The file extension of interest.
        """
        query = self._file_extension_query()
        return self._execute_query(query, (ext_param,))

    def query_by_event_type(self, event_type: str) -> list:
        """Queries the database by event type.
        Args:
            event_type (str): The event type of interest.
        """
        query = self._event_type_query()
        return self._execute_query(query, (event_type,))

    def query_by_event_location(self, event_location: str) -> list:
        """Queries the database by event location.
        Args:
            event_location (str): The event location of interest.
        """
        query = self._event_location_query()
        return self._execute_query(query, (f"{event_location}%",))

    def query_by_event_date(self, start_time: int, end_time: int) -> list:
        """Queries the database by event date.
        Args:
            start_time (int): The start time of interest. Should be in integer form
                (e.g., epoch time).
            end_time (int): The end time of interest. Should be in integer form
                (e.g., epoch time).
        """
        query = self._event_date_query()
        return self._execute_query(query, (start_time, end_time))

    def _execute_query(self, query: str, params: Optional[tuple] = None) -> list:
        conn = self.create_database_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except sqlite3.Error as e:
            raise sqlite3.DatabaseError(f"Database error: {e}")

    def close_connection(self) -> None:
        """Closes the database connection."""
        if self.__conn:
            self.__conn.close()
            self.__conn = None


    """Queries are defined below. All queries are private methods that return the SQL as
        a string. THe SQL must be parameterized.
    """

    def _create_table_sql(self) -> str:
        """Holds query string for creating table."""

        sql = """
        CREATE TABLE If NOt EXISTS file_events (
	      "event_id"	INTEGER NOT NULL,
	      "event_time"	INTEGER NOT NULL,
	      "event_type"	TEXT NOT NULL,
	      "event_location"	TEXT NOT NULL,
	      "file_type"	INTEGER,
	      "move_destination"	TEXT,
	      PRIMARY KEY("event_id" AUTOINCREMENT)
        );
        """
        return sql

    def _insert_data_sql(self) -> str:
        """returns SQL query for inserting data into the file_events table"""
        return """
        
        INSERT INTO file_events (
            event_time,
            event_type,
            event_location,
            file_type,
            move_destination
        )
        VALUES (?, ?, ?, ?, ?)
        """

    def _file_extension_query(self) -> str:
        """returns SQL query for selecting by file extension"""
        sql = """
        SELECT
            event_time,
            event_type,
            event_location,
            file_type,
            move_destination

        FROM  file_events
        Where file_type = ?
        """
        return sql

    def _event_type_query(self) -> str:
        """returns SQL query for selecting by action type"""
        sql = """
        SELECT
            event_time,
            event_type,
            event_loccation,
            file_type,
            move_destination

        FROM  file_events
        Where event_type = ?
        """
        return sql

    def _event_location_query(self) -> str:
        """returns SQL query for selecting by event location"""
        sql = """
        SELECT
            event_time,
            event_type,
            event_location,
            file_type,
            move_destination

        FROM  file_events
        WHERE event_location LIKE ?
        """
        return sql

    def _event_date_query(self) -> str:
        """returns SQL query for selecting by event date"""
        sql = """
        SELECT
            event_location,
            event_type,
            event_time,
            file_type,
            move_destination

        FROM  file_events
        WHERE event_time BETWEEN ? AND ?
        """
        return sql
