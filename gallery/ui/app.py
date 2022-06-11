from flask import Flask, request, render_template, redirect
from gallery.tools.db import connect, list_users, get_user, add_user, edit_user, delete_user, check_for_user


app = Flask(__name__)
connect()

@app.route('/admin')
def admin():
    users = list_users()
    return render_template('admin.html', users=user_helper(users))

@app.route('/admin/adduser')
def addUser():
    return render_template("adduser.html")

@app.route('/admin/add_user_execute', methods=['POST'])
def add_user_execute():
    username = request.form['username']
    password = request.form['password']
    full_name = request.form['full_name']
    add_user(username, password, full_name)

    return redirect('/admin')

@app.route('/admin/edit_user/<username>', methods=['GET'])
def edituser(username):
    db = get_user(username).fetchone()
    user = {'username': db[0], 'password': db[1], 'full_name': db[2]}
    return render_template('edituser.html', user=user)

@app.route('/admin/edit_user_execute/<username>', methods=['POST'])
def edit_user_execute(username):
    full_name = request.form['full_name']
    password = request.form['password']
    username = username


    edit_user(username, password, full_name)

    return redirect('/admin')

@app.route('/admin/deleteuser/<username>', methods=['GET'])
def deletion_user_check(username):
    return render_template("deleteuser.html", user=username)

@app.route('/admin/delete_user_confirm/<username>', methods=['POST'])
def delete_user_confirm(username):
    delete_user(username)
    return redirect('/admin')


def user_helper(users):
    result = []
    for row in users:
        result.append({'username': row[0], 'full_name':row[2]})
    return result
