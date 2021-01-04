import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


def Generate_Key(password):

    password = password.encode()
    mysalt = b'\xb7\x1f\x90\xca9\x05\xb1\xfb\xf3\xeb\xc1\xf9\xd1\xfdlV'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32,
        salt=mysalt,
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key.decode()


def encrypt(key, file_name):
    cypher = Fernet(key)
    with open(file_name, 'rb') as file:
        e_file = file.read()

    encrypted_file = cypher.encrypt(e_file)

    with open(file_name, "wb") as file:
        file.write(encrypted_file)

def decrypt(key, file_name):
    cypher = Fernet(key)
    with open(file_name , "rb") as file:
        encyrpted_data = file.read()

    decrypted_data = cypher.decrypt(encyrpted_data)
    with open(file_name, "wb") as file:
        file.write(decrypted_data)

if __name__ == "__main__":    
    key = Generate_Key("password")
    encrypt(key, "Database.csv")
