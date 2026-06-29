import os
import socket

from flask import Flask

from extensions import login_manager, set_database_path
from routes import app as app_routes

socket.setdefaulttimeout(5)

app = Flask(__name__)

database_url = os.environ.get('DATABASE_URL', 'database.db')
if database_url.startswith("sqlite:///"):
    database_url = database_url[len("sqlite:///"):]

set_database_path(database_url)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super-secret-random-key-here')

login_manager.init_app(app)

login_manager.login_view = "main.login"

app.register_blueprint(app_routes)

# Import after set_database_path so models.get_db() uses the right file.
from models import Book, User, init_db

with app.app_context():
    init_db()

    if not Book.first():
        books = [
            {"image": "itends.jpg", "title": "It Ends With Us",
             "description": "romance novel that explores the complexities of love, and the impact of difficult choices in a woman's life",
             "price": "25", "author": "Colleen Hoover"},
            {"image": "star.jpg", "title": "The Five-Star",
             "description": "a surprising and captivating story about friendship, love, and self-discovery set on Nantucket.",
             "price": "30", "author": "Elin Hilderbrand"},
            {"image": "view.jpg", "title": "You With A View",
             "description": "Romances of JulyTwo high school enemies must reunite for a road trip inspired by their grandparents' broken engagement",
             "price": "20", "author": "Jessica Joyce"},
            {"image": "crown.jpg", "title": "Ghosted",
             "description": "waited for a phone call that didn't come. Imagine you meet a man, spend six glorious days together, and fall in love",
             "price": "20", "author": "Amanda Quain"},
            {"image": "wife.jpg", "title": "The Hating Game",
             "description": "an executive assistant, locks horns with her colleague, they find themselves attracted to each other.",
             "price": "30", "author": "Sally Thorm"},
            {"image": "tessa.jpg", "title": "Unfortunately Yours",
             "description": "back in Napa Valley with this hilarious rom-com about a down-on-her-luck heiress who suggests a mutually beneficial marriage",
             "price": "25", "author": "Tessa Bailey"},
        ]
        for book in books:
            Book(image=book["image"], title=book["title"], description=book["description"],
                 price=book["price"], author=book["author"]).create()

    if not User.get_by_username("admin_user"):
        User(username="admin_user", password="lizidora", role="admin").create()

if __name__ == "__main__":
    app.run(debug=True)