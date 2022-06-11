import psycopg2
import json
from secrets import get_secret_image_gallery
from db import *

connection = None

def connect():
    global connection
    secret = get_secret()
    connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret), password=get_password(secret))

def execute(query, args=None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor

def temp_ui():

    exit_loop = False
    connect()

    while not exit_loop:
        print("\n 1) List users \n 2) Add user \n 3) Edit user \n 4) Delete user \n 5) Quit")

        choice = int(input("Enter command>"))

        if choice == 1:
            list_users()

        elif choice == 2:
            add_username = input("Username>")
            add_pass = input("Password>")
            add_fn = input("Full name>")

            if check_for_user(add_username):
                print("Error: user with username " + add_username + " already exists.")
            else:
                add_user(add_username, add_pass, add_fn)

        elif choice == 3:
            edit_username = input("Username to edit>")

            if check_for_user(edit_username):
                edit_pass = input("New password (press enter to keep current)>")
                edit_full_name = input("New full name (press enter to keep current)>")
                edit_user(edit_username, edit_pass, edit_full_name)

            else:
                print("No such user.")


        elif choice == 4:

            delete_username = input("Enter username to delete>")
            check = input("Are you sure you want to delete " + delete_username + "? ")

            if check.lower() == "yes" or "y":
                delete_user(delete_username)
                print("Deleted.")


        elif choice == 5:
            print("Bye")
            exit_loop = True


def main():
    connect()
    temp_ui()


if __name__ == '__main__':
    main()
