from flask import render_template,session,request,redirect
from . import app
from app.models import User

@app.route('/login',methods=["GET"])
def login():
	if 'userId' in session and User.isUser(session['userId']):
		return redirect('/')
	return render_template('auth/login.html',session=session)

@app.route('/signUp',methods=["GET"])
def signUp():
	if 'userId' in session and User.isUser(session['userId']):
		return redirect('/')
	return render_template('auth/signUp.html',session=session)