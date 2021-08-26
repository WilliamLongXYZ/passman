#!/bin/python
import base64
import getpass
import hashlib
import os


def new_user(username, password):
    salt = os.urandom(64)

    key = hashlib.pbkdf2_hmac(
        'sha512',                       # The hash digest algorithm for HMAC
        password.encode('utf-8'),       # Convert the password to bytes
        salt,                           # Provide the salt
        1000000                         # It is recommended to use at least 100,000 iterations of SHA-256 
    )
    storage = salt + key
    return storage

def get_key(username):
    with open('store.csv', 'r') as file:
        for row in file:
            row = row.split(',')
            if row[0] == username:
                storage = base64.b64decode(row[1])
                return storage[:64], storage[64:]

def check_pass(username, password):
    salt_from_store, key_from_store = get_key(username)
    key = hashlib.pbkdf2_hmac('sha512',password.encode('utf-8'),salt_from_store,1000000)
    check = 1 if key == key_from_store else False
    return check

def check_user(username):
    with open('store.csv', 'r') as file:
        for row in file:
            if username in row:
                return 1

def store_password(username, storage):
    storage = base64.b64encode(storage).decode('utf-8')
    with open(f'store.csv', 'a') as store:
        store.write(f'{username},{storage}\n')
    with open(f'{username}.csv', 'w') as db:
        db.write('service,website,email,username,password\n')

def login(username, password):
    if not os.path.isfile('store.csv'):
        with open('store.csv', 'w') as store:
            store.write("username,password\n")
    if not check_user(username):
        print("User does not exist.")
        store_password(username, new_user(username, password))
    return 1

def add_pass(user):
    service = input("What service will this password be for?")
    webaddress = input("What is the website of this service?")
    email = input("What email address did you use for this account?")
    username = input("What is your username for this service?")
    password = getpass.getpass("What is your password for this service?")
    with open(f'{user}.csv', 'a') as db:
        db.write(f'{service},{webaddress},{email},{username},{password}\n')

def main():
    while 1:
        username = input("What is your username?    ")
        password = getpass.getpass("What is your password?    ")
        if not login(username, password): return 0
        break
    while 1:
        input("Welcome to XerPassMan.")
        operation = input("Would you like to edit, add, or remove an entry?")
        if operation.lower() == 'add':
            add_pass(username)
        with open(f'{username}.csv', 'a') as db:
            if operation.lower() == 'edit':
                print("Edit.")
                db.write("Test")
                return 0
            if operation.lower() == 'remove':
                print("Remove.")
                return 0


if __name__ == '__main__':
    main()
