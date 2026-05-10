#MSSQL DB Helper
import os,pymssql
from enum import Enum, auto

from pymongo import MongoClient
from bson import ObjectId



class db_Types(Enum):
    MSSQL = auto()
    POSTGRESQL = auto()

class DBHelper:
    def __init__(self, db_type=db_Types.MSSQL):
        self.server = os.getenv('DB_SERVER', 'localhost')
        self.db_type = db_type
        if self.db_type == db_Types.MSSQL:
            self.database = os.getenv('DB_NAME', 'FProject')
            self.username = os.getenv('DB_USERNAME', 'sa')
            self.password = os.getenv('DB_PASSWORD')
        elif self.db_type == db_Types.POSTGRESQL:
            self.database = os.getenv('DB_NAME', 'FProject')
            self.username = os.getenv('DB_USERNAME', 'postgres')
            self.password = os.getenv('DB_PASSWORD')
        else:
            raise ValueError("Unsupported database type")

    def connect(self):
        if self.db_type == db_Types.MSSQL:
            return pymssql.connect(server=self.server, user=self.username, password=self.password, database=self.database)
        elif self.db_type == db_Types.POSTGRESQL:
            return MongoClient(f"mongodb://{self.username}:{self.password}@{self.server}/{self.database}")
        else:
            raise ValueError("Unsupported database type")
        
    def get_user_by_username(self, username):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                if self.db_type == db_Types.MSSQL:
                    cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
                elif self.db_type == db_Types.POSTGRESQL:
                    raise NotImplementedError("PostgreSQL support is not implemented yet")
                else:
                    raise ValueError("Unsupported database type")
                result = cursor.fetchone()
                if result:
                    return {"id": result[0], "username": result[1], "password": result[2]}
                return None


