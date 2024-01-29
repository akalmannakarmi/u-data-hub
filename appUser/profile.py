from flask import render_template, session, request, redirect,jsonify
from flask_login import login_required,current_user,login_user,logout_user
from . import app

@app.route('/myProfile')
def myProfile():
    userData = getUserData(session['userId'])
    return render_template('myProfile.html',session=session,userData=userData)


@app.route('/myProfile/<category>/edit',methods=["POST"])
def edit():
    userData = getUserData(session['userId'])
    return render_template('myProfile.html',session=session,userData=userData)


