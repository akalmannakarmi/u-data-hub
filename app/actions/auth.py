from flask import render_template,session,request,redirect,jsonify
from . import app
from app import db
from app.models import User
import bcrypt

@app.route('/login',methods=["POST"])
def login():
	if 'userId' in session and User.isUser(session['userId']):
		return redirect('/')
	
	data = request.form.deepcopy()
	rq=['username','password','next']
	if any(i not in data for i in rq):
		result = {"Require":{','.join(rq)}}
		return jsonify(result)

	user = User.query.filter_by(username=data['username']).first()
	if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password):
		session['userId']=user.id
		return redirect(request.form.get("next"))
	
	return redirect('/login?error=Incorrect username or password')

@app.route('/signUp',methods=["POST"])
def signUp():
	if 'userId' in session and User.isUser(session['userId']):
		return redirect('/')
	
	data = request.form.deepcopy()
	
	rq=['username','userTag','password']
	if any(i not in data for i in rq):
		result = {"Require":{','.join(rq)}}
		return jsonify(result)
		
	if len(data['username']) > 64:
		return redirect('/signUp?error=username too long')

	hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
	new_user = User(username=data['username'],password=hashed_password)
	db.session.add(new_user)
	db.session.commit()

	return redirect('/login')

@app.route('/logout',methods=["GET","POST"])
def logout():
    session.pop('userId')
    return redirect('/login')