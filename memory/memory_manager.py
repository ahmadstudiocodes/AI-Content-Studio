import sqlite3
from pathlib import Path


class MemoryManager:

    def __init__(self):

        Path("database").mkdir(exist_ok=True)

        self.conn = sqlite3.connect("database/studio.db")

        self.cursor = self.conn.cursor()

        self.initialize()

    def initialize(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS memories(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            category TEXT,

            key TEXT,

            value TEXT,

            created_at TEXT

        )

        """)

        self.conn.commit()

    def save(self, category, key, value, created_at):

        self.cursor.execute(

            """
            INSERT INTO memories
            (category,key,value,created_at)
            VALUES(?,?,?,?)
            """,

            (category, key, value, created_at)

        )

        self.conn.commit()

    def get(self, key):

        self.cursor.execute(

            "SELECT value FROM memories WHERE key=?",

            (key,)

        )

        row = self.cursor.fetchone()

        if row:

            return row[0]

        return None


memory = MemoryManager()