import psycopg2
import config, connect
import string, secrets, argparse

password_length = 20

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
    if not check_entry_exists(cursor, URL):
        SQL = "INSERT INTO passwords VALUES (%s, %s, %s)"
        cursor.execute(SQL, (URL, username, password))
        query_one(cursor, URL)
        print("Entry succesfully inserted.\n")
    else:
        print("There is already an account attached to the given URL.")

# Update an existing entry to the database
def update(cursor, URL, username):
    if check_entry_exists(cursor, URL):
        SQL = "UPDATE passwords SET username = %s WHERE url = %s"
        cursor.execute(SQL, (username, URL))
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

parser = argparse.ArgumentParser(
                    prog='Password Manager',
                    description='A program to store and manage passwords securely.')

parser.add_argument("-a", "--add", nargs=2, metavar=('URL', 'Username'),
                    help="Adds an entry with provided URL and username. Strong password will be automatically generated for the account. There is not support for multiple accounts on the same URL.")
parser.add_argument("-r", "--remove", nargs=1, metavar='URL',
                    help="Remove an entry by URL. If account attached to URL does not exists it will print an error message.")
parser.add_argument("-l", "--lookup", nargs="?", metavar='URL', default = 'all',
                    help="Lookup an entry by URL or query all entries. If provided with *all* or none it will print all entries.")
parser.add_argument("-u", "--update", nargs=2, metavar=('URL', 'Username'),
                    help="Update a username entry by URL. If account attached to URL does not exists it will print an error message.")

arguments = parser.parse_args()

# Add entry to the database
if arguments.add:
    password = create_password(password_length)
    insert(db_cursor, arguments.add[0], arguments.add[1], password)

# Remove entry from the databse
elif arguments.remove:
    remove(db_cursor, arguments.remove[0])

# Update entry in the database
elif arguments.update:
    update(db_cursor, arguments.update[0], arguments.update[1])

# Query the databse
else:
    if arguments.lookup == 'all' or arguments.lookup == None:
        query_all(db_cursor)
    else:
        query_one(db_cursor, arguments.lookup)

# Push any changes to the database
db_connect.commit()

#Close Communication with database
db_cursor.close()
