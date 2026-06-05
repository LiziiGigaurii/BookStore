# app.py
from flask import Flask
from extensions import db, mail, login_manager
from routes import main_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.config['SECRET_KEY'] = 'super-secret-random-key-here'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'gigaurilizi1238@gmail.com'
app.config['MAIL_PASSWORD'] = 'vhctxocrdrxpujlp'

db.init_app(app)
mail.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "main.login"

app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)