import sqlite3
from pathlib import Path


class MemoryStorage:

    def __init__(self):

        Path("database").mkdir(exist_ok=True)

        self.conn = sqlite3.connect("database/studio.db")

        self.cursor = self.conn.cursor()

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS memory(

            id INTEGER PRIMARY KEY,

            category TEXT,

            key TEXT,

            value TEXT,

            created TEXT

        )

        """)

        self.conn.commit()

    def save(self,item):

        self.cursor.execute(

            """

            INSERT INTO memory

            (category,key,value,created)

            VALUES(?,?,?,?)

            """,

            (

                item.category,

                item.key,

                item.value,

                item.created

            )

        )

        self.conn.commit()

    def search(self,key):

        self.cursor.execute(

            "SELECT value FROM memory WHERE key=?",

            (key,)

        )

        row=self.cursor.fetchone()

        return row


storage=MemoryStorage()