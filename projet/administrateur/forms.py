from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField, PasswordField
from wtforms.validators import DataRequired, Email


class AddSalleForm(FlaskForm):
    type_sal = SelectField('Type : ', choices=[('AMPHITHEATRE', 'AMPHITHEATRE'),
                                               ('SALLE D\'INFORMATIQUE', 'SALLE D\'INFORMATIQUE'),
                                              ('LABORATOIRE D\'ELECTRONIQUE', 'LABORATOIRE D\'ELECTRONIQUE'),
                                               ('LABORATOIRE D\'ELECTROTECHNIQUE', 'LABORATOIRE D\'ELECTROTECHNIQUE'),
                                              ('LABORATOIRE DE PHYSIQUE', 'LABORATOIRE DE PHYSIQUE'),
                                               ('LABORATOIRE DE CHIMIE', 'LABORATOIRE DE CHIMIE'),
                                               ('LABORATOIRE DE KINESITHERAPIE', 'LABORATOIRE DE KINESITHERAPIE'),
                                               ('LABORATOIRE DE SCIENCES INFIRMIER', 'LABORATOIRE DE SCIENCES INFIRMIER'),
                                               ('LABORATOIRE DE TECHNIQUE DE LABORATOIRE', 'LABORATOIRE DE TECHNIQUE DE LABO')])
    numero = StringField('Numero de salle : ')
    nbre_place = StringField('Nombre de places : ')
    submit = SubmitField('Confirmer')


class AddMaterielForm(FlaskForm):
    type_mat = SelectField('Type : ', choices=[('VIDEOPROJECTEUR', 'VIDEOPROJECTEUR'), ('HAUT-PARLEUR', 'HAUT-PARLEUR')])
    sn = StringField('Numero de serie : ')
    model = StringField('Model : ')
    exigence = RadioField('Exigences : ', choices=[('VGA', 'VGA'), ('USB', 'USB'),
                                                  ('HDMI', 'HDMI'), ('WIFI', 'WIFI')])
    submit = SubmitField('Confirmer')


class NewAdminForm(FlaskForm):
    nom = StringField('Nom d\'utilisateur : ')
    email = StringField('Email : ', validators=[DataRequired(), Email(message='Veuillez entrer un email valide')])
    password = PasswordField('Mot de passe : ', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')


class NewUserForm(FlaskForm):
    username = StringField('Nom d\'utilisateur : ')
    email = StringField('Email : ', validators=[DataRequired(), Email(message='Veuillez entrer un email valide')])
    matricule = PasswordField('Matricule : ', validators=[DataRequired()])
    poste = SelectField('Poste : ', choices=[('CHEF DE DEPARTEMENT','CHEF DE DEPARTEMENT'),
                                             ('ENSEIGNANT','ENSEIGNANT')])
    submit = SubmitField('Enregistrer')


class RechercheForm(FlaskForm):
    cri = StringField()
    submit = SubmitField('Rechercher')


class ResetForm(FlaskForm):
    reset = SubmitField('Reset')
