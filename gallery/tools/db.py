import psycopg2
import json
from .secrets import get_secret_image_gallery

#db_name = "image_gallery"
#db_user = "image_gallery"

#password_file = "/home/ec2-user/.image_gallery_config"

connection = None

def get_secret():
    jsonString = get_secret_image_gallery()
    return json.loads(jsonString)


def get_password(secret):
    return secret['password']


def get_host(secret):
    return secret['host']


def get_username(secret):
    return secret['username']


def get_dbname(secret):
    return secret['database_name']


def connect():
    global connection
    secret = get_secret()
    connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret),
                                  password=get_password(secret))


def execute(query, args=None):
    global connection
    connect()
    cursor = connection.cursor()
    connection.set_session(autocommit=True)
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor


def list_users():
    global connection
    connect()
    users = execute('SELECT * FROM users')
    return users

    #columns = [i[0] for i in cursor.description]

    #print(columns)
    #print("-------------------------------")
    #for row in users:
    #    print(row)

def get_user(username):
    username = execute('select * from users where username=%s', (username,))
    return username


def add_user(user_name, password, full_name):
    global connection
    connect()
    """add user to databse"""
    connect()
    cursor = connection.cursor()
    connection.set_session(autocommit=True)
    cursor.execute('INSERT INTO users VALUES (%s, %s, %s)', (user_name, password, full_name,))


def edit_user(user_name, password, full_name):
    """edit user, refactor later with snazzier way to accept enters"""

    if password != "":
        pw_update = """UPDATE users SET password = %s where username = %s"""
        execute(pw_update, (password, user_name))

    if full_name != "":
        fn_update = """UPDATE users SET full_name = %s where username = %s"""
        execute(fn_update, (full_name, user_name))


def delete_user(user_name):
    global connection
    connect()
    """delete user"""
    cursor = connection.cursor()
    connection.set_session(autocommit=True)
    cursor.execute('DELETE FROM users WHERE username = %s;', (user_name,))



def check_for_user(user_name):
    global connection
    connect()
    """check if user is in db?"""
    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(*) FROM users WHERE username = %s', [user_name])
    n, = cursor.fetchone()
    if n == 1:
        return True

#def get_password():
#    f = open(password_file, "r")
#    result = f.readline()
#    f.close()
#    return result[:-1]


#def execute(query, args=None):
#    global connection
#    cursor = connection.cursor()
#    if not args:
#        cursor.execute(query)

#    else:
#       cursor.execute(query, args)
#    return cursor

def main():
    connect()
    res = execute('select * from users')
    for row in res:
        print(row)
    # = execute("update users set password=%s where username= 'fred'", ('banana',))
    #res = execute('select * from users')
    #for row in res:
    #    print(row)

if __name__ == '__main__':
    main()

