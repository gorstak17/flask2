from flask import Flask, render_template,redirect, url_for, request, session
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import hashlib
import time

import mysql.connector
app = Flask(__name__)
app.config['SECRET_KEY'] = 'januar2021'
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="",
	database="februar2021"
    )
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')
 
@app.route('/register',methods=["POST", "GET"])
def register():
	if request.method=="GET":
		return render_template('register.html')	

	username = request.form['username']
	email = request.form['email']
	password = request.form['password']
	confirmpassword = request.form['confirmpassword']
	godinastudija = request.form['godinastudija']
	jmbg = request.form['jmbg']

	mc=mydb.cursor()
	mc.execute(f"SELECT *FROM korisnici WHERE username = '{username}'")
	rez = mc.fetchall()
	if len(rez) != 0:
		return "Username je zauzet!"
	if password != confirmpassword:
		return "Sifre se ne poklapaju"
	if len(jmbg) != 13:
		return "JMBG nema 13 karaktera"
	return redirect (url_for('show_all'))

@app.route('/login',methods=["POST", "GET"])
def login():
		if request.method == "GET":
			return render_template ('login.html')
		if 'username' in session:
			return "Vec ste ulogovali" 
		username = request.form['username']
		password = request.form['password']
		mc=mydb.cursor()
		mc.execute(f"SELECT *FROM korisnici WHERE username = '{username}'")
		rez = mc.fetchall()
		if len(rez) ==0:
			return "Korisnik ne postoji"
		if rez [0][5] != password:
			return "Sifra nije tacna"
		session ['username'] = username 
		return redirect (url_for('show_all'))
@app.route('/logout')
def logout ():
	if 'username' not in session:
		 return redirect(url_for('show_all'))
	session.pop ('username' , None)
	return redirect(url_for('login'))
@app.route ('/show_all')
def show_all():
	mc=mydb.cursor()
	mc.execute("SELECT * FROM korisnici")
	rez = mc.fetchall()
	return render_template ("/show_all.html", korisnici = rez)
@app.route ('/update/<username>')
def update(username):
	if request.method == "GET":
		mc=mydb.cursor()
		mc.execute(f"SELECT * FROM korisnici WHERE username = '{username}'")
		rez = mc.fetchall()
		if len(rez) == 0:
			return "Korisnik ne postoji"
			return render_template('update.html', korisnici=rez)
		email = request.form ['email']
		password = request.form ['password']
		godina = request.form['godina']
		mc=mydb.cursor()
		mc.execute(f"SELECT * FROM korisnici WHERE username = '{username}'")
		rez = mc.fetchall()

@app.route('/delete/<username>')
def delete(username):
	if 'username' not in session:
		return redirect (url_for('login'))
		mc = mydb.cursor()
	mc.execute(f"DELETE FROM korisnici WHERE username = '{username}'")
	mydb.commit()
	return redirect(url_for('show_all'))
	@app.route('/show_year/<year>')
	def show_year(year):
		mc = mydb.cursor()
	mc.execute(f"SELECT * FROM korisnici WHERE godina = '{year}'")
	rez = mc.fetchall()
	if len(rez) == 0:
		return "Nema nijedan student"
	return render_template('show_all.html', korisnici = rez)
		
		





		

	












if __name__ == '__main__':
	app.run(debug=True)