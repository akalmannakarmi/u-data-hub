from flask import render_template,session,request,redirect
from app.wrapers import isNotUser
from . import app

@app.route('/auth/login',methods=["GET"])
@isNotUser
def login():
	error=request.args.get('error') if request.args.get('error')!='None' else None
	next=request.args.get('next','/')
	print("next:",next)
	return render_template('_components/auth/login.html',session=session,next=next,error=error,rData={})

@app.route('/auth/signUp',methods=["GET"])
@isNotUser
def signUp():
	return render_template('_components/auth/signUp.html',session=session,rData={})