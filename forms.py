from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

from wtforms.fields import StringField, IntegerField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, length, equal_to, Email


class AddBookForm(FlaskForm):
    image = FileField("Upload an image", validators=[FileRequired()])
    title = StringField("book name", validators=[DataRequired()])
    description = TextAreaField("book description", validators=[DataRequired()])
    price = StringField("book price", validators=[DataRequired()])
    author = StringField("book author", validators=[DataRequired()])


    submit = SubmitField("Add book")


class EditBookForm(FlaskForm):
    image = FileField("Upload an image")
    title = StringField("book name", validators=[DataRequired()])
    description = TextAreaField("book description", validators=[DataRequired()])
    price = StringField("book price", validators=[DataRequired()])
    author = StringField("book author", validators=[DataRequired()])


    submit = SubmitField("Add book")



class ContactUsForm(FlaskForm):
    name = StringField("Enter your name", validators=[DataRequired()])
    email = StringField("Enter your email", validators=[DataRequired(), Email(message="Invalid email address.")])
    subject = StringField("Provide Context", validators=[DataRequired()])
    telephone = StringField("Provide Tel number", validators=[DataRequired()])
    yourmessage = TextAreaField("Write your question here", validators=[DataRequired()])

    submit = SubmitField("Send Message")


class RegisterForm(FlaskForm):
    username = StringField("Enter Username", validators=[DataRequired()])
    password = PasswordField("Enter Password",
                             validators=[
                                 DataRequired(),
                                 length(min=8, max=64)
                             ])
    repeat_password = PasswordField("Repeat password",
                                    validators=[
                                        DataRequired(),
                                        equal_to("password", message="Passwords are not the same!")
                                    ])
    register = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Enter your username", validators=[DataRequired()])
    password = PasswordField("Enter Your password", validators=[DataRequired()])

    login = SubmitField("Log in")