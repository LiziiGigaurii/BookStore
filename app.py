import os
from flask import Flask
import socket
from extensions import db, mail, login_manager
from routes import main_bp

socket.setdefaulttimeout(5)

app = Flask(__name__)

database_url = os.environ.get('DATABASE_URL', 'sqlite:///database.db')

if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super-secret-random-key-here')
app.config['MAIL_SERVER'] = 'smtp-relay.brevo.com'
app.config['MAIL_PORT'] = 465             
app.config['MAIL_USE_TLS'] = False               
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'adbcb5001@smtp-brevo.com'
app.config['MAIL_PASSWORD'] = 'bsk4Zq7odOpHkwQ'

db.init_app(app)
mail.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "main.login"

app.register_blueprint(main_bp)

with app.app_context():
    db.create_all()
    
    from models import Book, User
    
    if not Book.query.first():
        books = [
            {
                "image": "itends.jpg",
                "title": "It Ends With Us",
                "description": "romance novel that explores the complexities of love, and the impact of difficult choices in a woman's life",
                "price": "25",
                "author": "Colleen Hoover",
            },
            {
                "image": "star.jpg",
                "title": "The Five-Star",
                "description": "a surprising and captivating story about friendship, love, and self-discovery set on Nantucket.",
                "price": "30",
                "author": "Elin Hilderbrand",
            },
            {
                "image": "view.jpg",
                "title": "You With A View",
                "description": "Romances of JulyTwo high school enemies must reunite for a road trip inspired by their grandparents’ broken engagement",
                "price": "20",
                "author": "Jessica Joyce",
            },
            {
                "image": "crown.jpg",
                "title": "Ghosted",
                "description": "waited for a phone call that didn't come. Imagine you meet a man, spend six glorious days together, and fall in love",
                "price": "20",
                "author": "Amanda Quain",
            },
            {
                "image": "wife.jpg",
                "title": "The Hating Game",
                "description": "an executive assistant, locks horns with her colleague, they find themselves attracted to each other.",
                "price": "30",
                "author": "Sally Thorm",
            },
            {
                "image": "tessa.jpg",
                "title": "Unfortunately Yours",
                "description": "back in Napa Valley with this hilarious rom-com about a down-on-her-luck heiress who suggests a mutually beneficial marriage",
                "price": "25",
                "author": "Tessa Bailey",
            }
        ]
        for book in books:
            new_book = Book(image=book["image"], title=book["title"], description=book["description"], price=book["price"], author=book["author"])
            db.session.add(new_book)
        db.session.commit()

    if not User.query.filter_by(username="admin_user").first():
        admin_user = User(username="admin_user", password="lizi", role="admin")
        admin_user.create()

if __name__ == "__main__":
    app.run(debug=True)