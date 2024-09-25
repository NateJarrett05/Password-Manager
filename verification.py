import super_secret as ss
import argon2, getpass
from cryptography.fernet import Fernet

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

    print("✰✰✰ Welcome home Mr. Stark ✰✰✰")
    return True

def encrypt_password(raw_password):
    fernet = Fernet(ss.MASTER_KEY)
    encrypted_password = fernet.encrypt(raw_password.encode())
    return encrypted_password

def decrypt_password(encoded_password):
    fernet = Fernet(ss.MASTER_KEY)
    decrypted_password = fernet.decrypt(encoded_password).decode()
    return decrypted_password
