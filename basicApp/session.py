from flask import render_template, session, request, redirect,jsonify
from flask_login import login_required,current_user,login_user,logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from . import app


# Create database object
db = SQLAlchemy()

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template('signup.html',rData={})
    
    data = request.form.deepcopy()
    rq=['username','email','0password']
    if any(i not in data for i in rq):
        result = f"Require:{','.join(rq)}"
        return jsonify(result)

    new_user = User(username=data['username'],email=data['email'],password=data['0password'])

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        column = str(e.orig).split('.')[-1].replace('\'', '').replace('\"', '').split('.')[-1].strip()
        if column == 'email':
            return render_template('signup.html',rData=data,error="Email already exists")
        elif column == 'username':
            return render_template('signup.html',rData=data,error="Username already exists")
        else:
            return render_template('signup.html',rData=data,error="Unexpected Error")

    return redirect('/login')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html',rData={})
    
    data = request.form.deepcopy()
    rq=['email','0password']
    if any(i not in data for i in rq):
        result = f"Require:{','.join(rq)}"
        return jsonify(result)
    
    user = User.query.filter_by(email=data['email']).first()
    if user and user.password == data['0password']:
        session['username'] = user.username

        login_user(user,remember=True)
        if request.args.get("next"):
            return redirect(request.args.get("next"))
        return redirect('/')
    
    return render_template('login.html', rData=data,error="Invalid username or password")

@app.route('/logout',methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect('/login')


def init_app(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()