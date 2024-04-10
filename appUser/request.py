from flask import render_template, session, request, redirect,jsonify
from . import app,db

@app.route('/myProfile/request',methods=["GET"])
def requeste():
    if 'userId' not in session:
        return redirect('/login')
    
    categoriesAndFields = db.getCategoriesAndFields()
    return render_template('user/myProfile.html',session=session,categoriesAndFields=categoriesAndFields)
