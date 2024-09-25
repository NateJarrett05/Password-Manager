import psycopg2
import config, connect, functions, verification
import argparse

PASSWORD_LENGTH = 20

verified = verification.user_verification()

if(verified):
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
                        help="Update a username entry by URL and username. If account attached to URL does not exists it will print an error message.")
    arguments = parser.parse_args()

    # Add entry to the database
    if arguments.add:
        password = functions.create_password(PASSWORD_LENGTH)
        functions.insert(db_cursor, arguments.add[0], arguments.add[1], password)

    # Remove entry from the databse
    elif arguments.remove:
        functions.remove(db_cursor, arguments.remove[0])

    # Update entry in the database
    elif arguments.update:
        functions.update(db_cursor, arguments.update[0], arguments.update[1])

    # Query the databse
    else:
        if arguments.lookup == 'all' or arguments.lookup == None:
            functions.query_all(db_cursor)
        else:
            functions.query_one(db_cursor, arguments.lookup)

    # Push any changes made to the database
    db_connect.commit()

    # Close Communication with database
    db_cursor.close()
