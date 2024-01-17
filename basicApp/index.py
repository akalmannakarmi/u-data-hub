from flask import render_template,session,request,redirect
from . import app

@app.route('/')
@app.route('/index',methods=["GET"])
def index():
    if 'username' not in session:
        return redirect('/login')
    
    return render_template('index.html',session=session)