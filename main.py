from flask import Flask
from appBasic import app as APP_B,init as init_B
from appUser import app as APP_U,init as init_U

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

app.register_blueprint(APP_B)
app.register_blueprint(APP_U)
init_B(app)
init_U(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)