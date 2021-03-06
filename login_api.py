from urllib import response
from django.http import JsonResponse
from django.shortcuts import redirect, render
from flask import Flask, request, jsonify, make_response, send_from_directory, send_file, render_template, url_for
import os
import flask
from flask_cors import CORS
import pandas as pd
import numpy as np
import requests
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = '34.82.202.78'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'seng401'
app.config['MYSQL_DB'] = 'applytics'

CORS(app)
mysql = MySQL(app)

@app.route('/signup', methods = ['POST', 'GET'])
def signup():

    print("signup")

    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    atPos = email.find('@')
    domain = email[atPos+1:]

    company = domain[0:domain.find('.')]

    if(company == "gmail" or company == "yahoo" or company =="ucalgary" or company == "hotmail"):
        company = "N/A"

    print(company)



    cur0 = mysql.connection.cursor()
    result = cur0.execute("Select * FROM USERCREDENTIALS")

    if (result > 0):
        userDetails = cur0.fetchall()
        for user in userDetails:
            if (user[1] == email or user[0] == username):
                return jsonify({'status':'user already exists.'}), 401

    mysql.connection.commit()
    cur0.close()

    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO USERCREDENTIALS(email,username, password) VALUES(%s,%s,%s)""", (email,username,password))
    mysql.connection.commit()
    cur.close()
    return jsonify({'username': username, "company":company, "email":email}), 201


@app.route('/signupStoreDB', methods= ['POST'])
def storeSignupToDB():


    return jsonify({'status':'success'}), 201



@app.route('/login', methods = ['POST'])
def signin():
    print("signin")

    print(request.json)

    email = request.json["email"]
    password = request.json["password"]
    print("email is " + str(email))
    atPos = email.find('@')
    domain = email[atPos+1:]

    company = domain[0:domain.find('.')]

    print(company)

    print("Reached here   "+email)

    cur = mysql.connection.cursor()
    result = cur.execute("Select * FROM USERCREDENTIALS")

    if(result>0):

        userDetails = cur.fetchall()
        for user in userDetails:
            if(user[1]==email and user[2]==password):
                print("user is " +str(user[0]))
                return jsonify({'username': user[0], "company":company, "email":user[1]}), 200

    return jsonify({'error':'No valid account with credentials found!'}), 401


@app.route('/changePassword', methods = ['PUT'])
def changePassword():
    print("changePassword")

    print(request.json)

    username = request.json["username"]
    email = request.json["email"]
    oldPassword = request.json["oldPassword"]
    newPassword = request.json["newPassword"]

    if newPassword == oldPassword:
        return {'error': 'Old password is same as new password'}, 400

    cur = mysql.connection.cursor()
    result = cur.execute("Select * FROM USERCREDENTIALS")
    if(result > 0):
        userDetails = cur.fetchall()
        for user in userDetails:
            if (user[0] == username and user[1] == email and user[2] == oldPassword):
                cur.execute("UPDATE USERCREDENTIALS SET password = %s WHERE username = %s", [newPassword, username])
                mysql.connection.commit()
                cur.close()
                return jsonify({'username': username}), 200

    return jsonify({'error':'No valid account with credentials found!'}), 401


@app.route('/changeUsername', methods = ['PUT'])
def changeUsername():
    print("changeUsername")

    print(request.json)

    newUsername = request.json["newUsername"]
    oldUsername = request.json["oldUsername"]
    email = request.json["email"]
    password = request.json["password"]

    if newUsername == oldUsername:
        return {'error': 'Old username is same as new username'}, 400


    cur = mysql.connection.cursor()
    result = cur.execute("Select * FROM USERCREDENTIALS")
    if(result > 0):
        userDetails = cur.fetchall()
        for user in userDetails:
            if (user[0] == oldUsername and user[1] == email and user[2] == password):
                cur.execute("UPDATE USERCREDENTIALS SET username = %s WHERE username = %s", [newUsername, oldUsername])
                mysql.connection.commit()
                cur.close()
                return jsonify({'username': newUsername}), 200

    return jsonify({'error':'No valid account with credentials found!'}), 401


@app.route('/changeEmail', methods = ['PUT'])
def changeEmail():
    print("changeEmail")

    print(request.json)

    username = request.json["username"]
    newEmail = request.json["newEmail"]
    oldEmail = request.json["oldEmail"]
    password = request.json["password"]

    if oldEmail == newEmail:
        return {'error': 'Old email is same as new email'}, 400

    cur = mysql.connection.cursor()
    result = cur.execute("Select * FROM USERCREDENTIALS")
    if(result > 0):
        userDetails = cur.fetchall()
        for user in userDetails:
            if (user[0] == username and user[1] == oldEmail and user[2] == password):
                cur.execute("UPDATE USERCREDENTIALS SET email = %s WHERE email = %s", [newEmail, oldEmail])
                mysql.connection.commit()
                cur.close()
                return jsonify({'email': newEmail}), 200

    return jsonify({'error':'No valid account with credentials found!'}), 401


@app.route('/signinGetDB', methods= ['POST'])
def getSiginDB():

    email = request.json["email"]
    password = request.json["password"]

@app.route("/deleteUser", methods= ['DELETE'])
def deleteUser():
    username = request.json["username"]
     # delete in database
    cur = mysql.connection.cursor()
    cur.execute("""DELETE FROM USERCREDENTIALS WHERE username=%s""", (username,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
    print("Version: 1.0");
    app.run(host=os.getenv('IP','0.0.0.0'), port=int(os.getenv('PORT',5000)))
