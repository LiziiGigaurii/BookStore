from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

mail = Mail()
login_manager = LoginManager()
db = SQLAlchemy()

app = Flask(__name__)
app.config["SECRET_KEY"] = "5e5rtyG%RYTGuguu"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"


login_manager = LoginManager(app)
login_manager.login_view = "login"