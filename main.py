#!/usr/bin/python
import base64
import getpass
import hashlib
import os

import cryptography.fernet


# TODO: add edit option +feature

def main():
    cfg_dir = "~/.config/xerpassman/"
    if not os.path.isdir(cfg_dir): os.makedirs(cfg_dir)
    if not os.path.isfile(f"{cfg_dir}settings.txt"): generate_settings(cfg_dir)
    while 1:
        usr = input("What is your username?  ")
        passwd = getpass.getpass("What is your password?  ")
        login(usr, passwd)
        if not check_pass(usr, passwd): return 0
        break
    usr_dir = f"{cfg_dir}{usr}/"
    if not os.path.isdir(usr_dir): os.makedirs(usr_dir)
    keyfile = read_settings(username, cfg_dir)
    open_db(usr, passwd, keyfile)
    input("Welcome to XerPassMan.")
    while 1:
        ops = {'add': add_pass, 'remove': remove_pass, 'list': list_pass, 'exit': encrypt}
        operation = input("Would you like to list, edit, add, remove an entry, or exit the program?  ")
        ops[operation](usr, passwd, keyfile)
        if operation.lower == 'exit': return

def generate_settings(cfg_dir):
    kf = input("Would you like to use a keyfile for increased security? Currently, without a keyfile, your passwords will remain unencrypted.  ")
    kf = 'true' if kf == 'yes' else 'false'
    if kf == 'true':
        kf_type = input("Would you like your keyfile to be individual or shared?  ")
        if kf_type == 'individual':
            kf_name = input("Would you like the keyfile to contain the user's name?  ")
            kf_name = 'user' if kf == 'yes' else 'filekey'
        kf_location = input("Where would you like to store your keyfile? Leave blank for the default of ~/.config/xerpassman. Enter 'user' if you want each user to have a seperate directory.     ")
        if kf_location == 'user': kf_location == 'user-dirs'
        elif not kf_location: kf_location == 'default'
    db_location = input("Where would you like to store your database? This has the same default location and options as keyfile.    ")
    if db_location == 'user': db_location == 'user-dirs'
    elif not db_location: db_location = 'default'
    store_location = input("Where would you like to store logins for XerPassMan? Leave blank for a default of ~/.config/xerpassman. ")
    if not store_location: store_location = 'default'
    settings = f"keyfile={kf}\n"
    if kf == 'true':
        settings += f"keyfile_type={kf_type}\n"
        if kf_type == 'individual': settings += f"keyfile_name={kf_name}\n"
        settings += f"keyfile_location={kf_location}\n"
    settings += f"db_location={db_location}\nstore_location={store_location}\n"
    with open(f"{cfg_dir}settings.txt", 'w') as setting_file: setting_file.write(settings)

def read_settings(usr, cfg_dir, usr_dir, *options):
    with open(f"{cfg_dir}settings.txt", 'r') as settings: lines = settings.readlines()
    for line in lines:
        if 'keyfile=false' in line: return 0
        if 'keyfile_type=individual' in line: file_extension = 'key'
        if 'keyfile_name=user' in line: keyname = f"{usr}.{file_extension}"
        elif "keyfile_name=filekey" in line: keyname = f"filekey.{file_extension}"
        if 'keyfile_location=user' in line: keyfile_location = f"{usr_dir}{keyname}"
    return keyfile_location

def login(user, passwd):
    if not os.path.isfile('store.csv'):
        with open('store.csv', 'w') as store: store.write("username,password\n")
    if not check_user(user):
        print("User does not exist.")
        store_password(user, new_user(passwd))

def check_user(username):
    with open('store.csv', 'r') as file:
        for row in file:
            if username in row: return 1

def new_user(passwd):
    salt = os.urandom(64)
    key = hashlib.pbkdf2_hmac('sha512',passwd.encode('utf-8'),salt,1048576)
    return salt + key

def store_password(usr, storage):
    storage = base64.b64encode(storage).decode('utf-8')
    with open(f'store.csv', 'a') as store: store.write(f'{usr},{storage}\n')
    with open(f'{usr}.csv', 'w') as db: db.write('service,webaddress,email,username,password\n')

def check_pass(usr, passwd):
    salt_from_store, key_from_store = get_key(usr)
    key = hashlib.pbkdf2_hmac('sha512',passwd.encode('utf-8'),salt_from_store,1048576)
    check = 1 if key == key_from_store else 0
    return check

def get_key(usr):
    with open('store.csv', 'r') as file:
        for row in file:
            row = row.split(',')
            if row[0] == usr:
                storage = base64.b64decode(row[1])
                return storage[:64], storage[64:]

def open_db(usr, passwd, keyfile=None):
    if determine_key_type(keyfile):
        if not os.path.isfile(keyfile): generate_keyfile(usr, keyfile)
        with open(keyfile, 'rb') as filekey: key = filekey.read()
    else: 
        with open (keyfile, 'r') as keydb:
            for row in keydb:
                row = row.split()
                if row[0] == usr: key = row[-1]
    fernet = cryptography.fernet.Fernet(key)
    db = f"{usr}.csv"
    with open(db, 'rb') as encrypted_file: encrypted = encrypted_file.read()
    try: decrypted = fernet.decrypt(encrypted)
    except: return
    with open(db, 'wb') as decrypted_file: decrypted_file.write(decrypted)

def determine_key_type(kf):
    kf = kf.split('.')[-1]
    if kf == 'csv': return 0
    elif kf == 'key': return 1

def generate_keyfile(usr, path):
    key = cryptography.fernet.Fernet.generate_key()
    if determine_key_type(path):
        with open(path, 'wb') as filekey: filekey.write(key)
    else: generate_keydb(usr, key)

def generate_keydb(usr, key):
    if not os.isfile('keydb.csv'):
        with open(f"keydb.csv", 'w') as db: db.write("username,key\n")
    with open(f"keydb.csv", 'w') as db: db.write(f"{usr},{key}")

def add_pass(xpass_usr, *tmp):
    service = input("What service will this password be for?  ")
    webaddress = input("What is the website of this service?  ")
    email = input("What email address did you use for this account?  ")
    username = input("What is your username for this service?  ")
    passwd = getpass.getpass("What is your password for this service?  ")
    with open(f'{xpass_usr}.csv', 'a') as db: db.write(f'{service},{webaddress},{email},{username},{passwd}\n')

def remove_pass(xpass_usr, *tmp):
    webaddress = input("What webaddress did you store this under?  ")
    email = input("What is the email you put in with this service?  ")
    username = input("What username did you assign to this?  ")
    with open(f'{xpass_usr}.csv', "r+") as db:
        lines = db.readlines()
        db.seek(0)
        for i in lines:
            if f"{webaddress},{email},{username}" not in i: db.write(i)
        db.truncate()

def list_pass(usr, *tmp):
    with open(f'{username}.csv', 'r') as db: lines = db.readlines
    for i in lines: print(i)

def encrypt(usr, passwd, keyfile):
    if not keyfile: return 0
    with open(keyfile, 'r') as filekey: key = filekey.read()
    with open(f"{usr}.csv", 'rb') as db: original = db.read()
    with open(f"{usr}.csv", 'wb') as to_encrypt:
        to_encrypt.write(cryptography.fernet.Fernet(key).encrypt(original))


if __name__ == '__main__':
    main()
