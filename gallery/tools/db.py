import psycopg2
import os
import json

#db_name = "image_gallery"
#db_user = "image_gallery"

#password_file = "/home/ec2-user/.image_gallery_config"

db_host = os.getenv('PG_HOST')
db_name = os.getenv('IG_DATABASE')
db_user = os.getenv('IG_USER')

def get_db_password():
    file = open(os.getenv('IG_PASSWD_FILE'), 'r')
    password = file.readline()
    return password.strip()

connection = None

#def get_secret():
#    jsonString = get_secret_image_gallery()
#    return json.loads(jsonString)


#def get_password(secret):
#    return secret['password']


#def get_host(secret):
#    return secret['host']


#def get_username(secret):
#    return secret['username']


#def get_dbname(secret):
#    return secret['database_name']

def get_user_password(username):
    global connection
    connect()
    cursor = connection.cursor()
    connection.set_session(autocommit=True)

    cursor.execute('select username, password, full_name from users where username = %s', (username,))
    row = cursor.fetchone()
    if row is None:
        return None
    else:
        return row[1]


def connect():
    global connection
    secret = get_secret()
    connection = psycopg2.connect(host=db_host, dbname=db_name, user=db_user,
                                  password=get_db_password())


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

def get_images(user):
   connect()
   images = "select file, user, image_id from images where user=(%s)"
   results = execute(images, (user,))
   image_list = []
   for row in results:
       image = Image(row[0], row[1], row[2])
       image_list.append(image)
   return image_list

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

