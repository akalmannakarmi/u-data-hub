from flask import render_template,session,request,redirect,jsonify
from flask_login import LoginManager,login_required,login_user,logout_user
from flask_sqlalchemy import SQLAlchemy
from . import app,dbBasic


# Create database object
db = SQLAlchemy()

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<User %r>' % self.username
    
    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True 

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template('basic/signup.html',rData={})
    
    data = request.form.deepcopy()
    rq=['username','userTag','password']
    if any(i not in data for i in rq):
        result = f"Require:{','.join(rq)}"
        return jsonify(result)
    
    if len(data['username']) > 50:
        return render_template('basic/signup.html',rData=data,error="Username too long. Max 50")
    elif len(data['password']) > 100:
        return render_template('basic/signup.html',rData=data,error="Password too long. Max 100")

    new_user = User(username=data['username'],password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    dbBasic.addUser(new_user.id,data['userTag'])

    return redirect('/login')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('basic/login.html',rData={})
    
    data = request.form.deepcopy()
    print(data)
    rq=['username','password']
    if any(i not in data for i in rq):
        result = f"Require:{','.join(rq)}"
        return jsonify(result)
    
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        session['userId']=user.id

        login_user(user,remember=True)
        if request.args.get("next"):
            return redirect(request.args.get("next"))
        return redirect('/')
    
    return render_template('basic/login.html', rData=data,error="Invalid username or password")

@app.route('/logout',methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect('/login')


def init_app(app):
    login_manager = LoginManager(app)
    login_manager.login_view = 'basicApp.login'
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))