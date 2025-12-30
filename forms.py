from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp

class StudentForm(FlaskForm):
    fname = StringField("First Name", validators=[DataRequired(), Length(min=2, max=50)])
    lname = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[
        DataRequired(),
        Regexp(r'^[0-9]{10,15}$', message="Enter a valid phone number")
    ])
    city = StringField("City", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Add")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Login")

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = StringField("Message", validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField("Submit")
