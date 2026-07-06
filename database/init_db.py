from database.database import db


def initialize():

    db.execute("""

    CREATE TABLE IF NOT EXISTS projects(

        id INTEGER PRIMARY KEY,

        name TEXT,

        created TEXT

    )

    """)

    db.execute("""

    CREATE TABLE IF NOT EXISTS channels(

        id INTEGER PRIMARY KEY,

        name TEXT,

        platform TEXT

    )

    """)

    print("Database Ready.")