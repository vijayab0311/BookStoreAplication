from flask import Flask

from flask_mysqldb import MySQL





app = Flask(__name__)
app.secret_key = "Firstbit"

from urls import *

if __name__ == "__main__":
    app.run(debug=True)