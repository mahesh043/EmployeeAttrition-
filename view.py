from flask import Flask, redirect, render_template, request, session, url_for

import pickle 
from flask_mysqldb import MySQL
import pandas as pd
import MySQLdb.cursors
import re
app = Flask(__name__)

app.secret_key = 'xyzjkabc'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'eswar'

mysql = MySQL(app)
 
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return render_template('index.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)

@app.route('/logout')
def logout():
   session.pop('loggedin',None)
   session.pop('userid',None)
   session.pop('password',None)
   return redirect(url_for('login'))

@app.route('/signup',methods = ['POST', 'GET'])
def signup():
   mesage = ''
   if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
      userName = request.form['name']
      password = request.form['password']
      email = request.form['email']
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
      account = cursor.fetchone()
      if account:
         mesage = 'Account already exists !'
      elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
         mesage = 'Invalid email address !'
      elif not userName or not password or not email:
         mesage = 'Please fill out the form !'
      else:
         cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (userName, email, password, ))
         mysql.connection.commit()
         mesage = 'You have successfully registered !'
   elif request.method == 'POST':
      mesage = 'Please fill out the form !'
   return render_template('signup.html', mesage = mesage)

@app.route('/index',methods = ['POST', 'GET'])
def index():
   return render_template('index.html')
 
@app.route('/result',methods = ['POST', 'GET'])
def result():
   
   # employee_id = request.form['employee_id']
   # return f"Employee ID: {employee_id}"
   if request.method == 'POST':
      result = request.form
      select=request.form.get('department')
      salary=request.form.get('salary')
      #model=pickle.load(open('final_prediction.pickle',"rb"))
      model=pickle.load(open('final_prediction.pickle',"rb"))
      g=pd.DataFrame(result,index=[0])
      g['department']=select
      g['salary']=salary
      
      
      res=model.predict(g)
   

      return render_template("result.html",result=res)
 
      

if __name__ == '__main__':
   app.run(debug = True,port=6001)
