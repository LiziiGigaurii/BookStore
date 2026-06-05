# models.py
from extensions import db, login_manager
from random import randint

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def save(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model, BaseModel, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # Added unique=True to prevent duplicate usernames in the database backend
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    role = db.Column(db.String)

    def __init__(self, username, password, role="guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Book(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String)
    title = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.String)
    author = db.Column(db.String)


if __name__ == "__main__":
    from app import app

    with app.app_context():
        db.create_all()

        # 1. Safeguard: Only add books if the Book table is empty
        if not Book.query.first():
            print("Seeding books into the database...")
            books = [
                {
                    "id": 1,
                    "image": "itends.jpg",
                    "title": "It Ends With Us",
                    "description": "romance novel that explores the complexities of love, and the impact of difficult choices in a woman's life",
                    "price": 25,
                    "author": "Colleen Hoover",
                },
                {
                    "id": 2,
                    "image": "star.jpg",
                    "title": "The Five-Star",
                    "description": "a surprising and captivating story about friendship, love, and self-discovery set on Nantucket.",
                    "price": 30,
                    "author": "Elin Hilderbrand",
                },
                {
                    "id": 3,
                    "image": "view.jpg",
                    "title": "You With A View",
                    "description": "Romances of JulyTwo high school enemies must reunite for a road trip inspired by their grandparents’ broken engagement",
                    "price": 20,
                    "author": "Jessica Joyce",
                },
                {
                    "id": 4,
                    "image": "crown.jpg",
                    "title": "Ghosted",
                    "description": "waited for a phone call that didn't come. Imagine you meet a man, spend six glorious days together, and fall in love",
                    "price": 20,
                    "author": "Amanda Quain",
                },
                {
                    "id": 5,
                    "image": "wife.jpg",
                    "title": "The Hating Game",
                    "description": "an executive assistant, locks horns with her colleague, they find themselves attracted to each other.",
                    "price": 30,
                    "author": "Sally Thorm",
                },
                {
                    "id": 6,
                    "image": "tessa.jpg",
                    "title": "Unfortunately Yours",
                    "description": "back in Napa Valley with this hilarious rom-com about a down-on-her-luck heiress who suggests a mutually beneficial marriage",
                    "price": 25,
                    "author": "Tessa Bailey",
                }
            ]

            for book in books:
                new_book = Book(image=book["image"], title=book["title"], description=book["description"],
                                price=book["price"], author=book["author"])
                db.session.add(new_book)
            db.session.commit()
            print("Books seeded successfully!")
        else:
            print("Books already exist in the database. Skipping book seed.")

        # 2. Safeguard: Only add the admin if they don't exist yet
        if not User.query.filter_by(username="admin_user").first():
            print("Creating admin user...")
            admin_user = User(username="admin_user", password="lizi", role="admin")
            admin_user.create()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists. Skipping admin creation.")