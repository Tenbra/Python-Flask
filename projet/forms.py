from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email(message='Veuillez entrer un email valide')])
    password = PasswordField('Mot de passe: ', validators=[DataRequired()])
    submit = SubmitField('Connexion')
