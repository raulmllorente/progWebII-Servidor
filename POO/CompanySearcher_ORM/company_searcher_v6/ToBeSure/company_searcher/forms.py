from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, HiddenField#, SelectField,
from wtforms.validators import InputRequired, Length, Email,EqualTo

class SearchForm(FlaskForm):
    company_name = StringField('Entrar el nombre de la empresa que deseas buscar: ')

class RegisterForm(FlaskForm):
    username = StringField("User Name / Nombre de usuario", validators=[InputRequired(),Length(min=4,max=15)])
    email = StringField("E-mail", validators=[InputRequired(),Email(message="Email no es válido!"),Length(max=50)])
    password = PasswordField("Password / Contraseña ",
    validators=[InputRequired(), Length(min=4), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Confirm password / Confirmar contraseña ", validators=[InputRequired()])

class LoginForm(FlaskForm):
    username_or_email = StringField('Enter your username or your email / Entre su usuario o e-mail')
    password = PasswordField('Password / Contraseña', validators=[InputRequired(),Length(min=4,max=80)])
    nextpath = HiddenField('Next Path')
    remember = BooleanField('Remember Me / Recuérdame')

class ResetPasswordForm(FlaskForm):
    email = StringField("E-mail", validators=[InputRequired(),Email(message="Email no es válido!"),Length(max=50)])


class SetNewPasswordForm(FlaskForm):
    username = HiddenField('username')
    userhash = HiddenField('userhash')
    password = PasswordField("Password / Contraseña ",validators=[InputRequired(), Length(min=4), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Confirm password / Confirmar contraseña ", validators=[InputRequired()])

