import sqlite3
from pathlib import Path


class Database:

    def __init__(self):

        Path("database").mkdir(
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            "database/studio.db"
        )

        self.cursor = self.connection.cursor()

    def execute(self, sql, params=()):

        self.cursor.execute(sql, params)

        self.connection.commit()

    def fetch(self, sql, params=()):

        self.cursor.execute(sql, params)

        return self.cursor.fetchall()


db = Database()