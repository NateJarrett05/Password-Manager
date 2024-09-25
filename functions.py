import verification
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
            decoded_password = verification.decrypt_password(record[2])
            print("URL: " + record[0])
            print("Username: " + record[1])
            print("Password: " + decoded_password)
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
            print(record[2])
            decoded_password = verification.decrypt_password(record[2])
            print("URL: " + record[0])
            print("Username: " + record[1])
            print("Password: " + decoded_password)
            print("----------")

# Insert a new entry to the database
def insert(cursor, URL, username, password):
    if not check_entry_exists(cursor, URL):
        encrypted_password = verification.encrypt_password(password)
        SQL = "INSERT INTO passwords VALUES (%s, %s, %s)"
        cursor.execute(SQL, (URL, username, encrypted_password.decode()))
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
