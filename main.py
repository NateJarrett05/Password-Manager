import psycopg2

# Connect to an existing database
conn = psycopg2.connect(
    database = "pass_manager",
    user = "postgres",
    password = "password01",
    host = "0.0.0.0"
)

# Open cursor to perform database operatiosn
cur = conn.cursor()

#Query the database
cur.execute("SELECT * FROM passwords")
rows = cur.fetchall()

if not len(rows):
    print("Empty")
else:
    for row in rows:
        print(row)

#Close Communication with database
cur.close()
conn.close()
