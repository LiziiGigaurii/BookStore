import os
from flask import Flask
from extensions import db, mail, login_manager
from routes import main_bp

app = Flask(__name__)

database_url = os.environ.get('DATABASE_URL', 'sqlite:///database.db')

if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super-secret-random-key-here')
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

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)