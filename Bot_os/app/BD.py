import sqlite3


connection = sqlite3.connect("Mana.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER,
    name VARCHAR(30),
    wins INTEGER,
    cash INTEGER,
    phone INTEGER,
    car INTEGER,
    house INTEGER
    )
""")
connection.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin(
    user_id INTEGER,
    name VARCHAR(30)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS farm(
    user_id INTEGER,
    size INTEGER,
    lvl INTEGER
    )
""")

cursor.execute("""
                CREATE TABLE IF NOT EXISTS phone(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name_phone TEXT,
               price INTEGER
               )
""")

cursor.execute("""
                CREATE TABLE IF NOT EXISTS car(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT,
               price INTEGER
               )
""")

cursor.execute("""
                CREATE TABLE IF NOT EXISTS house(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price INTEGER
               )
""")

cursor.execute("""
                CREATE TABLE IF NOT EXISTS army(
               user_id INTEGER NOT NULL,
               soldiers INTEGER,
               cars INTEGER,
               tanks INTEGER
               )
""")