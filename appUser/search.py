from flask import render_template, session, request, redirect,jsonify
from . import app,db

@app.route('/search',methods=["GET"])
def search():
    if 'userId' not in session:
        return redirect('/login')
    
    tag=request.args.get('q',"",str)
    users=[]
    if tag:
        users=db.findUsers(tag)
    return render_template('user/search.html',session=session,users=users)