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

app.config['MYSQL_HOST'] = '35.185.241.182'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'seng401'
app.config['MYSQL_DB'] = 'applytics'

CORS(app)
mysql = MySQL(app)

@app.route('/signup', methods = ['POST', 'GET'])
def signup():

    print("signup")

    name = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    
    atPos = email.find('@')
    domain = email[atPos+1:]

    company = domain[0:domain.find('.')]

    if(company == "gmail" or company == "yahoo" or company =="ucalgary" or company == "hotmail"):
        company = "N/A"

    print(company)

    result = {"username": name, "email": email, "password": password, "company": company}
    
    response = requests.post("http://localhost:5000/signupStoreDB", json=result)

    print(response.status_code)

    if response.status_code == 201:
        return jsonify(result),201

    else:
        return jsonify({"status":"failed"}),401
    
    
@app.route('/signupStoreDB', methods= ['POST'])
def storeSignupToDB():
    print(request)
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']


    cur0 = mysql.connection.cursor()
    result = cur0.execute("Select * FROM USERCREDENTIALS")

    if (result > 0):
        userDetails = cur0.fetchall()
        for user in userDetails:
            if (user[1] == email or user[0] == username):
                return jsonify({'status':'user already exists.'}), 500

    mysql.connection.commit()
    cur0.close()

    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO USERCREDENTIALS(email,username, password) VALUES(%s,%s,%s)""", (email,username,password))
    mysql.connection.commit()
    cur.close()

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
                return jsonify({'username': user[0], "email":user[1], "password":user[2]}), 200

    return jsonify({'error':'No valid account found!'}), 401
   
   


@app.route('/signinGetDB', methods= ['POST'])
def getSiginDB():

    email = request.json["email"]
    password = request.json["password"]

    

if __name__ == "__main__":
    print("Version: 1.0");
    app.run(host=os.getenv('IP','0.0.0.0'), port=int(os.getenv('PORT',5000)))
