from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import TimeField
from wtforms.validators import DataRequired


class ReservationForm(FlaskForm):
    filiere = StringField("Filière : ", validators=[DataRequired()])
    salle = StringField('Salle : ', validators=[DataRequired()])
    matiere = StringField('Matiere : ', validators=[DataRequired()])
    h_debut = TimeField('De : ', validators=[DataRequired()])
    h_fin = TimeField('à : ', validators=[DataRequired()])

    submit1 = SubmitField('Reserver')


class RechercheForm(FlaskForm):
    critere = StringField()
    submit = SubmitField('Rechercher')