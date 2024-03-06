from data import db
from flask import Flask
from appBasic import app as APP_B,init as init_B
from appUser import app as APP_U,init as init_U
from appAdmin import app as APP_A,init as init_A
from appAPI import app as APP_API,init as init_API
import logging

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
logging.basicConfig(filename='logs/flask.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app.register_blueprint(APP_B)
app.register_blueprint(APP_U)
app.register_blueprint(APP_A)
app.register_blueprint(APP_API)
db.init()
init_B(app)
init_U(app)
init_A(app)
init_API(app)


if __name__ == "__main__":
    print("http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000,debug=True)