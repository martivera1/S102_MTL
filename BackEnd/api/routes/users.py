from functools import wraps
from flask import session, redirect, request, jsonify
from db.db import get_db
from routes.auth import login_required

# @login_required
def get_user():
    user_id = session.get('user_id')

    db = get_db()
    cursor = db.cursor()

    if request.method == "GET":

        query = """
        SELECT ID, email, name, sex, age, profile_picture FROM Users
        WHERE ID = %s
        """
        cursor.execute(query, (user_id,))
        users = cursor.fetchall()

        result = []
        for user in users:
            result.append({
                'ID': user[0],
                'email': user[1],
                'name': user[2],
                'sex': user[3],
                'age': user[4],
                'profile_picture': user[5]
            })

        cursor.close()
        return jsonify(result)

    elif request.method == "POST":

        data = request.json

        print(data)

        new_name = data.get('new_name')
        new_sex = data.get('new_sex')
        new_age = data.get('new_age')
        new_profile_picture = data.get('new_profile_picture')

        
        query = """
        UPDATE TABLE Users SET name = %s, sex = %s, age = %s, profile_picture = %s WHERE ID = %s
        """
        cursor.execute(query, (new_name, new_sex, new_age, new_profile_picture, user_id))
        db.commit()


        cursor.close()
        return


@login_required
def get_users():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT ID, email, name, sex, age, profile_picture FROM Users"
    cursor.execute(query)
    users = cursor.fetchall()

    result = []
    for user in users:
        result.append({
            'ID': user[0],
            'email': user[1],
            'name': user[2],
            'sex': user[3],
            'age': user[4],
            'profile_picture': user[5]
        })

    cursor.close()
    return jsonify(result)

def init_app(app):
    app.route('/users', methods=['GET'])(get_users)
    app.route('/profile', methods=['GET', 'POST'])(get_user)