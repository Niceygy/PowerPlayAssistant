from server.database.cycle import get_cycle_week
import sqlite3
from datetime import datetime, timedelta
from typing import Optional


class Cache:
    """
    Manages the cache sqlite database
    """

    def __init__(self):
        """
        Creates & starts the class
        """
        self.path = "cache/cache.db"
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA journal_mode=WAL;")
        # DEBUG
        # self.conn.set_trace_callback(print)
        # END DEBUG
        self.cycle_week = get_cycle_week()

    def __exit__(self) -> None:
        self.conn.commit()
        self.conn.close()
        return

    def clean(self, name: str):
        """
        Cleans old cache entries for the specified table
        """
        self.table_check(name)
        self.cursor.execute(f"DELETE FROM {name} WHERE expiry < {self.timestamp()};")

    def table_check(self, name: str) -> None:
        """
        Creates the table for that item, if it isn't already present
        """
        self.cursor.execute(
            f"""
                CREATE TABLE IF NOT EXISTS {name} (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    input TEXT,
                    data TEXT,
                    expiry INT,
                    cycle INT
                );"""
        )
        return

    def expiry(self, days: Optional[int]) -> int:
        """
        Calculates the expiry for a new entry.
        days can be adjusted as needed (default 7)
        """
        if days is None: days = 7
        time = datetime.now() + timedelta(days=days)
        return time.timestamp()

    def timestamp(self) -> int:
        """
        Returns a timestamp that is used in the SELECT statement for add() and get()
        If the expiry > timestamp(), it is valid.
        """
        return datetime.now().timestamp()
    
    def add(self, query: str, data: str, data_type: str, expiry_override: Optional[int]) -> None:
        """Adds an item to the cache

        Args:
            query (str): What was inputted to get the result. Used to search for it later
            data (str): The data that needs to be cached
            data_type (str): The data type. E.G raregoods or megaships
        """
        try:
            self.table_check(data_type)
            self.cursor.execute(
                f"SELECT * FROM {data_type} WHERE input = '{query}' AND cycle = '{self.cycle_week}' AND expiry > {self.timestamp()};"
            )
            result = self.cursor.fetchone()
            if result is None:
                self.cursor.execute(
                    f"INSERT INTO {data_type} (input, data, expiry, cycle) VALUES (?, ?, ?, ?)",
                    (query, data, self.expiry(expiry_override), self.cycle_week),
                )
                self.conn.commit()
            return
        except Exception:
            return

    def get(self, query: str, data_type: str) -> list:
        """Gets an item from the cache, if it exists

        Args:
            query (str): What was inputted to get the result.
            data_type (str): The data type. E.G raregoods or megaships

        Returns:
            list: The cached data
        """
        try:
            self.table_check(data_type)
            self.cursor.execute(
                f"SELECT data FROM {data_type} WHERE input = '{query}' AND cycle = '{self.cycle_week}' AND expiry > {self.timestamp()};"
            )
            result = self.cursor.fetchone()
            if result is None:
                return None
            else:
                return result
        except Exception as e:
            print(e)
            return None
