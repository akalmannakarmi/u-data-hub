from flask import Flask
from basicApp import app as APP,init

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

app.register_blueprint(APP)
init(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)