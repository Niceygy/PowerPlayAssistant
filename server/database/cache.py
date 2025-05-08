from server.database.cycle import get_cycle_week
import json
import ast
import sqlite3
from datetime import datetime, timedelta


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
        self.cycle_week = get_cycle_week()

    def __exit__(self) -> None:
        self.conn.commit()
        self.conn.close()
        return

    def table_check(self, name: str) -> None:
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

    def expiry(self) -> int:
        # all expiry is one week
        time = datetime.now() + timedelta(days=6, hours=23)
        return time.timestamp()

    def timestamp(self) -> int:
        """
        Returns a timestamp that is used in the SELECT statement for add() and get()
        If the expiry > timestamp(), it is valid.
        """
        return datetime.now().timestamp()

    def add(self, query: str, data: str, data_type: str) -> None:
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
                    (query, data, self.expiry(), self.cycle_week),
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


# def item_in_cache(system_name: str, shortcode: str, opposing: bool, dataType: str) -> str | None:
#     """
#     Is this thing in cache? If so, return it
#     """
#     current_week = get_cycle_week()
#     try:
#         with open(f"cache/week{current_week}.cache", "r") as f:
#             for line in f.read().splitlines():
#                 if line is None:
#                     continue
#                 if not line.startswith(f"{dataType}:"):
#                     continue
#                 else:
#                     line = line.removeprefix(f"{dataType}:")
#                 temp = line.split("/", 3)
#                 _system_name = temp[0]
#                 _shortcode = temp[1]
#                 _opposing = temp[2]
#                 _data = temp[3]
#                 if (
#                     _system_name == system_name
#                     and _shortcode == shortcode
#                     and _opposing == str(opposing)
#                 ):
#                     f.close()

#                     if dataType == "MEGASHIP":
#                         result = []
#                         jsonData = json.loads(_data)
#                         for entry in jsonData:
#                             megaship_name = entry[0]["name"]
#                             system = entry[0][f"SYSTEM{get_cycle_week()}"]
#                             result.append([megaship_name, system])
#                         return result
#                     else:
#                         return ast.literal_eval(_data)
#             f.close()
#     except FileNotFoundError:
#         with open(f"cache/week{current_week}.cache", "w") as f:
#             f.write("")
#             f.close()
#         return None
#     return None

# def add_item_to_cache(system_name: str, shortcode: str, opposing: bool, data: str, dataType: str):
#     """
#     Add this thing to the cache
#     """
#     if item_in_cache(system_name, shortcode, opposing, dataType) is not None:
#         return
#     else:
#         current_week = get_cycle_week()
#         with open(f"./cache/week{current_week}.cache", "a") as f:
#             f.write(f"{dataType}:{system_name}/{shortcode}/{opposing}/{json.dumps(data)}\n")
#             f.close()
#         return


def clean_caches():
    return
    for i in range(5):
        try:
            open(f"cache/week{i}.cache", "w").close()
        except FileNotFoundError:
            open(f"cache/week{i}.cache", "r").write(" ")
