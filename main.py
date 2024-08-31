import psycopg2

import string
import secrets
# Connect to an existing database
conn = psycopg2.connect(
    database = "pass_manager",
    user = "postgres",
    password = "password01",
    host = "0.0.0.0"
)

# Creates a password with at least one upper and lowercase letter + min 3 digits
def create_password(length):
    chars = string.ascii_letters + string.digits + '!@#$%^&*'
    while True:
        password = ''.join(secrets.choice(chars) for i in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password

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
