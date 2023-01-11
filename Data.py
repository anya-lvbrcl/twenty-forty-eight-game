import sqlite3

db = sqlite3.connect("game.sqlite")

cursor = db.cursor()

cursor.execute("""
create table if not exists ATTEMPTS(
    name text,
    score integer
)
""")


def saving(name, score):
    cursor.execute("""
          insert into ATTEMPTS values (?, ?)
      """, (name, score))
    db.commit()


def results():
    cursor.execute("""
    SELECT name Gamer, max(score) Score from ATTEMPTS
    GROUP by name
    ORDER by score DESC
    limit 3
    """)
    return cursor.fetchall()


#
# cursor.close()
