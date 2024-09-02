import psycopg2, string, secrets
import config
import connect

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

# Load the config from database.ini
db_config = config.load_config()

# Connect to an existing database with the config
db_connect = connect.connect(db_config);

# Open cursor to perform database operatiosn
cur = db_connect.cursor()

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
