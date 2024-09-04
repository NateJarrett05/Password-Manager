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

# Checks the databse for a given URL and returns if it exists
def check_entry_exists(cursor, URL):
    SQL = "SELECT * FROM passwords WHERE url = %s"
    cursor.execute(SQL, (URL,))
    entries = cursor.fetchone()
    if entries == None:
        print("No account found for the URL: " + URL)
        return False
    else:
        return True

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

# Insert a new entry to the database
def insert(cursor, URL, username, password):
    SQL = "INSERT INTO passwords VALUES (%s, %s, %s)"
    cursor.execute(SQL, (URL, username, password))
    query_one(cursor, URL)
    print("Entry succesfully inserted.\n")

# Update an existing entry to the database
def update(cursor, URL, username, password):
    if check_entry_exists(cursor, URL):
        SQL = "UPDATE passwords SET username = %s, password = %s WHERE url = %s"
        cursor.execute(SQL, (username, password, URL))
        query_one(cursor, URL)
        print("Entry succesfully updated.\n")

# Remove an existing entry from the database
def remove(cursor, URL):
    if check_entry_exists(cursor, URL):
        query_one(cursor, URL)
        SQL = "DELETE FROM passwords WHERE url = %s"
        cursor.execute(SQL, (URL,))
        print("Entry succesfully removed.\n")

# Load the config from database.ini
db_config = config.load_config()
# Connect to an existing database with the config
db_connect = connect.connect(db_config);
# Open cursor to perform database operatiosn
db_cursor = db_connect.cursor()

# Query the database
query_all(db_cursor)

# Modify the database
insert(db_cursor, "www.youtube.com", "username03", "password03")
update(db_cursor, "www.youtube.com", "username10", "password10")
remove(db_cursor, "www.youtube.com")

# Push any changes to the database
db_connect.commit()

#Close Communication with database
db_cursor.close()
