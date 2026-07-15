import sqlite3

from pathlib import Path



class MemoryStorage:

    """
    Arman StudioOS Memory Storage

    SQLite persistent storage
    for long-term memories.
    """



    def __init__(self):


        Path(
            "database"
        ).mkdir(
            exist_ok=True
        )


        self.conn = sqlite3.connect(

            "database/studio.db",

            check_same_thread=False

        )


        self.cursor = self.conn.cursor()


        self.initialize()



    # ==================================================

    def initialize(
        self
    ):


        self.cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS memory(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                category TEXT,

                key TEXT,

                value TEXT,

                created TEXT

            )

            """

        )


        self.cursor.execute(

            """

            CREATE INDEX IF NOT EXISTS idx_memory_key

            ON memory(key)

            """

        )


        self.conn.commit()



    # ==================================================

    def save(
        self,
        item
    ):


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



    # ==================================================

    def search(
        self,
        key
    ):


        self.cursor.execute(

            """

            SELECT

                category,

                key,

                value,

                created


            FROM memory


            WHERE key=?


            ORDER BY id DESC

            """,

            (

                key,

            )

        )


        rows = self.cursor.fetchall()


        return [

            {

                "category": row[0],

                "key": row[1],

                "value": row[2],

                "created": row[3]

            }

            for row in rows

        ]



    # ==================================================

    def delete(
        self,
        key
    ):


        self.cursor.execute(

            "DELETE FROM memory WHERE key=?",

            (

                key,

            )

        )


        self.conn.commit()



    # ==================================================

    def clear(
        self
    ):


        self.cursor.execute(

            "DELETE FROM memory"

        )


        self.conn.commit()



storage = MemoryStorage()