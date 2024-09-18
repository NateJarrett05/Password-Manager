import super_secret as ss
import argon2, getpass

# Verifies the user has permission to access the database with a password and key string
def user_verification():
    # Password verification
    ph = argon2.PasswordHasher()
    login_pass = getpass.getpass(prompt='Master Password: ')
    login_pass_hash = ph.hash(login_pass + ss.SALT)
    try:
        ph.verify(login_pass_hash, ss.SALTED_MASTER)
    except:
        print("Invalid master password. Intruder!")
        return False

    # Key verification
    login_key = getpass.getpass(prompt='Master Key: ')
    if(login_key != ss.MASTER_KEY):
        print("Invalid master key. Intruder!")
        return False

    print("Welcome home Mr. Stark\n")
    return True
