import sqlite3
import json

from pathlib import Path
from datetime import datetime



class MemoryManager:

    """
    Arman StudioOS Persistent Memory

    SQLite based long-term storage.

    Stores:

    - Agent knowledge
    - Workflow history
    - User preferences
    - System memories

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

            CREATE TABLE IF NOT EXISTS memories(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                category TEXT,

                key TEXT,

                value TEXT,

                created_at TEXT

            )

            """

        )


        self.cursor.execute(

            """

            CREATE INDEX IF NOT EXISTS idx_memory_key

            ON memories(key)

            """

        )


        self.conn.commit()



    # ==================================================

    def save(
        self,
        category,
        key,
        value,
        created_at=None
    ):


        if created_at is None:

            created_at = datetime.now().isoformat()



        if not isinstance(
            value,
            str
        ):

            value = json.dumps(
                value,
                ensure_ascii=False
            )



        self.cursor.execute(

            """

            INSERT INTO memories

            (category,key,value,created_at)

            VALUES(?,?,?,?)

            """,

            (
                category,
                key,
                value,
                created_at
            )

        )


        self.conn.commit()



    # ==================================================

    def get(
        self,
        key
    ):


        self.cursor.execute(

            """

            SELECT value

            FROM memories

            WHERE key=?

            ORDER BY id DESC

            LIMIT 1

            """,

            (
                key,
            )

        )


        row = self.cursor.fetchone()



        if not row:

            return None



        value = row[0]


        try:

            return json.loads(
                value
            )

        except:

            return value



    # ==================================================

    def get_all(
        self,
        category=None
    ):


        if category:


            self.cursor.execute(

                """

                SELECT key,value,created_at

                FROM memories

                WHERE category=?

                """,

                (
                    category,
                )

            )


        else:


            self.cursor.execute(

                """

                SELECT key,value,created_at

                FROM memories

                """

            )



        return self.cursor.fetchall()



    # ==================================================

    def delete(
        self,
        key
    ):


        self.cursor.execute(

            "DELETE FROM memories WHERE key=?",

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

            "DELETE FROM memories"

        )


        self.conn.commit()



    # ==================================================

    def close(
        self
    ):


        self.conn.close()



memory = MemoryManager()