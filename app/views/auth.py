from flask import render_template,session,request,redirect
from app.wrapers import isNotUser
from . import app

@app.route('/login',methods=["GET"])
@isNotUser
def login():
	error=request.args.get('error',None)
	next=request.args.get('next','/')
	return render_template('auth/login.html',session=session,error=error,next=next,rData={})

@app.route('/signUp',methods=["GET"])
@isNotUser
def signUp():
	return render_template('auth/signUp.html',session=session,error=None,rData={})