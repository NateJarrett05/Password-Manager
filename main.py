import psycopg2
import config, connect
import string, secrets

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

# Retrieve and print all entries from the database
def query_all(cursor):
    cursor.execute("SELECT * FROM passwords")
    entries = cursor.fetchall()
    if not len(entries):
        print("No passwords stored")
    else:
        print("----------")
        for record in entries:
            print("URL: " + record[0])
            print("Username: " + record[1])
            print("Password: " + record[2])
            print("----------")

# Retrieve and print entries fetched by URL
def query_one(cursor, URL):
    SQL = "SELECT * FROM passwords WHERE url = %s"
    cursor.execute(SQL, (URL,))
    entries = cursor.fetchall()
    if not len(entries):
        print("No account found for the URL: " + URL)
    else:
        print("----------")
        for record in entries:
            print("URL: " + record[0])
            print("Username: " + record[1])
            print("Password: " + record[2])
            print("----------")

# Load the config from database.ini
db_config = config.load_config()
# Connect to an existing database with the config
db_connect = connect.connect(db_config);
# Open cursor to perform database operatiosn
cur = db_connect.cursor()

#Query the database
query_all(cur)
query_one(cur, "www.google.com")

#Close Communication with database
cur.close()
