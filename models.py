from extensions import get_db, login_manager

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


def init_db():
    """Create tables if they don't already exist."""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'guest'
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT,
            title TEXT,
            description TEXT,
            price TEXT,
            author TEXT
        )
    """)
    conn.commit()
    conn.close()


class User(UserMixin):
    def __init__(self, id=None, username=None, password=None, role="guest", _hashed=False):
        self.id = id
        self.username = username
        self.password = password if _hashed else generate_password_hash(password)
        self.role = role

    def get_id(self):
        return str(self.id)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def create(self):
        conn = get_db()
        cur = conn.execute(
            "INSERT INTO user (username, password, role) VALUES (?, ?, ?)",
            (self.username, self.password, self.role),
        )
        conn.commit()
        self.id = cur.lastrowid
        conn.close()
        return self

    def save(self):
        conn = get_db()
        conn.execute(
            "UPDATE user SET username = ?, password = ?, role = ? WHERE id = ?",
            (self.username, self.password, self.role, self.id),
        )
        conn.commit()
        conn.close()

    def delete(self):
        conn = get_db()
        conn.execute("DELETE FROM user WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()

    @staticmethod
    def _from_row(row):
        if row is None:
            return None
        return User(id=row["id"], username=row["username"], password=row["password"],
                    role=row["role"], _hashed=True)

    @staticmethod
    def get(user_id):
        conn = get_db()
        row = conn.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        return User._from_row(row)

    @staticmethod
    def get_by_username(username):
        conn = get_db()
        row = conn.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
        conn.close()
        return User._from_row(row)

    @staticmethod
    def first():
        conn = get_db()
        row = conn.execute("SELECT * FROM user LIMIT 1").fetchone()
        conn.close()
        return User._from_row(row)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


class Book:
    def __init__(self, id=None, image=None, title=None, description=None, price=None, author=None):
        self.id = id
        self.image = image
        self.title = title
        self.description = description
        self.price = price
        self.author = author

    def create(self):
        conn = get_db()
        cur = conn.execute(
            "INSERT INTO book (image, title, description, price, author) VALUES (?, ?, ?, ?, ?)",
            (self.image, self.title, self.description, self.price, self.author),
        )
        conn.commit()
        self.id = cur.lastrowid
        conn.close()
        return self

    def save(self):
        conn = get_db()
        conn.execute(
            "UPDATE book SET image = ?, title = ?, description = ?, price = ?, author = ? WHERE id = ?",
            (self.image, self.title, self.description, self.price, self.author, self.id),
        )
        conn.commit()
        conn.close()

    def delete(self):
        conn = get_db()
        conn.execute("DELETE FROM book WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()

    @staticmethod
    def _from_row(row):
        if row is None:
            return None
        return Book(id=row["id"], image=row["image"], title=row["title"],
                    description=row["description"], price=row["price"], author=row["author"])

    @staticmethod
    def get(book_id):
        conn = get_db()
        row = conn.execute("SELECT * FROM book WHERE id = ?", (book_id,)).fetchone()
        conn.close()
        return Book._from_row(row)

    @staticmethod
    def all():
        conn = get_db()
        rows = conn.execute("SELECT * FROM book").fetchall()
        conn.close()
        return [Book._from_row(row) for row in rows]

    @staticmethod
    def first():
        conn = get_db()
        row = conn.execute("SELECT * FROM book LIMIT 1").fetchone()
        conn.close()
        return Book._from_row(row)


if __name__ == "__main__":
    init_db()

    print("Seeding books into the database..." if not Book.first() else "Books already exist. Skipping.")
    if not Book.first():
        books = [
            {"image": "itends.jpg", "title": "It Ends With Us",
             "description": "romance novel that explores the complexities of love, and the impact of difficult choices in a woman's life",
             "price": 25, "author": "Colleen Hoover"},
            {"image": "star.jpg", "title": "The Five-Star",
             "description": "a surprising and captivating story about friendship, love, and self-discovery set on Nantucket.",
             "price": 30, "author": "Elin Hilderbrand"},
            {"image": "view.jpg", "title": "You With A View",
             "description": "Romances of JulyTwo high school enemies must reunite for a road trip inspired by their grandparents’ broken engagement",
             "price": 20, "author": "Jessica Joyce"},
            {"image": "crown.jpg", "title": "Ghosted",
             "description": "waited for a phone call that didn't come. Imagine you meet a man, spend six glorious days together, and fall in love",
             "price": 20, "author": "Amanda Quain"},
            {"image": "wife.jpg", "title": "The Hating Game",
             "description": "an executive assistant, locks horns with her colleague, they find themselves attracted to each other.",
             "price": 30, "author": "Sally Thorm"},
            {"image": "tessa.jpg", "title": "Unfortunately Yours",
             "description": "back in Napa Valley with this hilarious rom-com about a down-on-her-luck heiress who suggests a mutually beneficial marriage",
             "price": 25, "author": "Tessa Bailey"},
        ]
        for book in books:
            Book(image=book["image"], title=book["title"], description=book["description"],
                 price=book["price"], author=book["author"]).create()
        print("Books seeded successfully!")

    if not User.get_by_username("admin_user"):
        print("Creating admin user...")
        User(username="admin_user", password="lizi", role="admin").create()
        print("Admin user created successfully!")
    else:
        print("Admin user already exists. Skipping admin creation.")