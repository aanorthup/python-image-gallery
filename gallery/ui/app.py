import os
from werkzeug.utils import secure_filename
from functools import wraps
from flask import Flask, flash, request, render_template, redirect, session, url_for
from gallery.tools.db import connect, list_users, get_user, add_user, edit_user, delete_user, check_for_user, get_user_password
from gallery.tools.flask_secret import get_secret_flask_session
from gallery.tools.image import Image
from gallery.tools.image_dao import ImageDAO
from gallery.tools.postgres_image_dao import PostgresImageDAO
from gallery.tools.s3 import *



app = Flask(__name__)
bucket = os.getenv("S3_IMAGE_BUCKET")
UPLOAD_FOLDER = bucket
file_types = {"tif", "jpg", "jpeg", "gif", "png"}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_flask_session():
    file = open(os.getenv('FLASK_SESSION_FILE'), 'r')
    session = file.readline()
    return session.strip()

app.secret_key = get_flask_session()

connect()


@app.route("/")
def main_menu():
    if session and session['username']:
        return render_template('main_menu.html', user=session['username'])
    else:
        return redirect('/login')

def check_admin():
    return 'username' in session and session['username'] == 'admin'

def check_user():
    return 'username' in session

@app.route('/admin')
def admin():
    if not check_admin():
        return redirect('/login')
    users = list_users()
    return render_template('admin.html', users=user_helper(users))

@app.route('/invalidLogin')
def invalidLogin():
    return "Invalid"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_password = get_user_password(request.form["username"])
        if user_password != request.form["password"] or user_password is None:
            return redirect('/invalidLogin')
        else:
            session['username'] = request.form["username"]
            return redirect("/")
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('main_menu'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in file_types


def get_image_dao():
    return PostgresImageDAO()


@app.route('/upload/<username>', methods=['GET', 'POST'])
def upload_file(username):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            if put_object(bucket, file.filename, file):
                get_image_dao().add_image(Image(file.filename, username))
            return redirect('/')
    return render_template('upload.html')

@app.route('/view_images/<username>')
def view_images(username):
    images = get_image_dao().get_images_by_username(username)
    if not images:
        return 'No images are currently uploaded! :('
    return render_template('view_images.html', user=username, images=images)









@app.route('/admin/users')
def users():
    if not check_admin():
        return redirect('/login')
    return render_template('admin.html', users=user_helper(users))


@app.route('/admin/adduser')
def addUser():
    if not check_admin():
        return redirect('/login')
    return render_template("adduser.html")

@app.route('/admin/add_user_execute', methods=['POST'])
def add_user_execute():
    if not check_admin():
        return redirect('/login')
    username = request.form['username']
    password = request.form['password']
    full_name = request.form['full_name']

    add_user(username, password, full_name)

    return redirect('/admin')

@app.route('/admin/edit_user/<username>', methods=['GET'])
def edituser(username):
    if not check_admin():
        return redirect('/login')
    db = get_user(username).fetchone()
    user = {'username': db[0], 'password': db[1], 'full_name': db[2]}
    return render_template('edituser.html', user=user)

@app.route('/admin/edit_user_execute/<username>', methods=['POST'])
def edit_user_execute(username):
    if not check_admin():
        return redirect('/login')
    full_name = request.form['full_name']
    password = request.form['password']
    username = username

    edit_user(username, password, full_name)

    return redirect('/admin')

@app.route('/admin/deleteuser/<username>', methods=['GET'])
def deletion_user_check(username):
    if not check_admin():
        return redirect('/login')
    return render_template("deleteuser.html", user=username)

@app.route('/admin/delete_user_confirm/<username>', methods=['POST'])
def delete_user_confirm(username):
    if not check_admin():
        return redirect('/login')
    delete_user(username)
    return redirect('/admin')


def user_helper(users):
    users = []
    for row in users:
        users.append({'username': row[0], 'full_name':row[2]})
    return users

def current_user():
    result = ""
    for key, value in session.items():
        return str(value)
