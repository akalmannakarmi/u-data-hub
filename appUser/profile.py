from flask import render_template, session, request, redirect,jsonify
from . import app,db

@app.route('/profile/<userTag>',methods=["GET"])
def viewProfile(userTag):
    userId = getUserId(userTag)
    userData = getUserData(userId)
    return render_template('viewProfile.html',session=session,userData=userData)

@app.route('/myProfile',methods=["GET"])
def myProfile():
    userData = getUserData(userId)
    return render_template('myProfile.html',session=session,userData=userData)

@app.route('/myProfile/<category>/add',methods=["POST"])
def add():
    userData = getUserData(session['userId'])
    return redirect('/myProfile')

@app.route('/myProfile/<category>/edit',methods=["POST"])
def edit():
    userData = getUserData(session['userId'])
    return redirect('/myProfile')

@app.route('/myProfile/<category>/remove',methods=["POST"])
def remove():
    userData = getUserData(session['userId'])
    return redirect('/myProfile')