from flask import Flask
from apps import app as APP,init

app = Flask(__name__)
app.register_blueprint(APP)
init(app)

if __name__ == "__main__":
    app.run(debug=True)