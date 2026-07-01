from flask import render_template, redirect, flash, Blueprint, current_app
from flask_login import login_user, logout_user, login_required, current_user
from os import path
from forms import AddBookForm, RegisterForm, LoginForm, EditBookForm, ContactUsForm
from models import Book, User

app = Blueprint('main', __name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/payment")
def payment():
    return render_template("payment.html")


@app.route("/books")
def booklist():
    books = Book.all()
    return render_template("books.html", books=books)


@app.route("/view_book/<int:book_id>")
def viewbook(book_id):
    book = Book.get(book_id)
    if not book:
        return render_template("404.html")
    return render_template("view_book.html", book=book)


@app.route("/publish_yours", methods=["GET", "POST"])
@login_required
def publish():
    form = AddBookForm()

    if form.validate_on_submit():
        file = form.image.data
        filename = file.filename
        file.save((path.join(current_app.root_path, 'static', filename)))

        new_book = Book(image=filename, title=form.title.data, description=form.description.data,
                        price=form.price.data, author=form.author.data)
        new_book.create()

        flash("Your book has been added successfully!")
        return redirect("/books")

    return render_template("publishpage.html", form=form)


@app.route("/edit_book/<int:book_id>", methods=["GET", "POST"])
@login_required
def edit_book(book_id):
    if current_user.role != "admin":
        return redirect("/")

    book = Book.get(book_id)
    if not book:
        return render_template("404.html")

    form = EditBookForm(title=book.title, description=book.description, price=book.price, author=book.author)
    if form.validate_on_submit():
        file = form.image.data
        if file:
            filename = file.filename
            file.save((path.join(current_app.root_path, 'static', filename)))
            book.image = filename

        book.title = form.title.data
        book.description = form.description.data
        book.price = form.price.data
        book.author = form.author.data

        book.save()

        return redirect("/books")

    return render_template("publishpage.html", form=form)


@app.route("/delete_book/<int:book_id>")
@login_required
def delete_book(book_id):
    if current_user.role != "admin":
        return redirect("/")

    book = Book.get(book_id)
    if not book:
        return render_template("404.html")

    book.delete()

    flash("Your book has been deleted successfully!")
    return redirect("/books")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.get_by_username(form.username.data)
        if existing_user:
            flash("Username already in use!")
        else:
            user = User(username=form.username.data, password=form.password.data)
            user.create()
            flash("registration completed!")
            return redirect("/register")

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("You successfully logged in!")
            return redirect("/")
        else:
            flash("Password is incorrect. Please try again.", "error")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("You successfully logged out of your account!")
    return redirect("/")


@app.route("/about_us")
def aboutus():
    return render_template("aboutus.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactUsForm()

    if form.validate_on_submit():
        flash("Your message has been received!")
        return redirect("/")

    return render_template("contactus.html", form=form)