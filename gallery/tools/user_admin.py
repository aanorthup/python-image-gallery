import psycopg2

db_host = "image-database.cnfajid7xjkb.us-east-1.rds.amazonaws.com"
db_name = "image_gallery"
db_user = "image_gallery"

password_file = "/home/ec2-user/.image_gallery_config"

connection = None

def get_password():
    f = open(password_file, "r")
    result = f.readline()
    f.close()
    return result[:-1]

def connect():
    global connection
    connection = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=get_password())

def execute(query, args=None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor

def list_users():
    cursor = connection.cursor()

    cursor.execute('select * from users')
    users = cursor.fetchall()

    columns = [i[0] for i in cursor.description]

    print(columns)
    print("-------------------------------")
    for row in users:
        print(row)

def add_user(user_name, password, full_name):
    """add user to databse"""
    cursor = connection.cursor()

    cursor.execute('INSERT INTO users VALUES (%s, %s, %s)', (user_name, password, full_name,))

    connection.commit()


def edit_user(user_name, password, full_name):
    """edit user, refactor later with snazzier way to accept enters"""
    cursor = connection.cursor()

    if password != "":
        pw_update = """UPDATE users SET password = %s where username = %s"""
        cursor.execute(pw_update, (password, user_name))
        connection.commit()


    if full_name != "":
        fn_update = """UPDATE users SET full_name = %s where username = %s"""
        cursor.execute(fn_update, (full_name, user_name))
        connection.commit()



def delete_user(user_name):
    """delete user"""
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users WHERE username = %s;', (user_name,))

    connection.commit()

def check_for_user(user_name):
    """check if user is in db?"""
    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(*) FROM users WHERE username = %s', [user_name])
    n, = cursor.fetchone()
    if n == 1:
        return True



def temp_ui():

    exit_loop = False

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
