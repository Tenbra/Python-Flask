from projet import db, login_manager
from flask_login import UserMixin


class Materiel(db.Model):
    __tablename__='Materiel'
    sn = db.Column(db.Text, primary_key=True, unique=True, index=True)
    type = db.Column(db.Text, index=True)
    model = db.Column(db.Text, index=True)
    exigence = db.Column(db.Text)
    reserv_id = db.Column(db.Integer, db.ForeignKey('ReservMateriel.id'))

    def __init__(self, sn, type, model, exigence):
        self.type = type
        self.sn = sn
        self.model = model
        self.exigence = exigence


class Salle(db.Model):
    __tablename__ = 'Salle'
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True)
    type = db.Column(db.Text, index=True)
    numero = db.Column(db.Text)
    nbre_place = db.Column(db.Integer)
    reserv_id = db.Column(db.Integer, db.ForeignKey('ReservSalle.id'))

    def __init__(self, type, numero, nbre_place):
        self.type = type
        self.numero = numero
        self.nbre_place = nbre_place


class HistoriqueMS(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True)
    type = db.Column(db.Text, index=True)
    uniq_id = db.Column(db.Text)
    info1 = db.Column(db.Text)
    info2 = db.Column(db.Text)
    statut = db.Column(db.Text)

    def __init__(self, type, uniq_id, info1, info2, statut):
        self.type = type
        self.uniq_id = uniq_id
        self.info1 = info1
        self.info2 = info2
        self.statut = statut


class ReservSalle(db.Model):
    __tablename__ = 'ReservSalle'
    salle = db.relationship('Salle', backref='salle', uselist=False)
    id = db.Column(db.Integer, primary_key=True)
    filiere = db.Column(db.Text)
    matiere = db.Column(db.Text)
    h_debut = db.Column(db.Text)
    h_fin = db.Column(db.Text)
    jour = db.Column(db.Text)
    statut = db.Column(db.Text)
    user = db.relationship('User', backref='reserveur_sal', uselist=False)

    def __init__(self, salle, filiere, matiere, h_debut, h_fin, statut, user):
        self.salle = salle
        self.filiere = filiere
        self.matiere = matiere
        self.h_debut = h_debut
        self.h_fin = h_fin
        self.statut = statut
        self.user = user


class ReservMateriel(db.Model):
    __tablename__ = 'ReservMateriel'
    materiel = db.relationship('Materiel', backref='materiel', uselist=False)
    id = db.Column(db.Integer, primary_key=True)
    filiere = db.Column(db.Text)
    matiere = db.Column(db.Text)
    h_debut = db.Column(db.Text)
    h_fin = db.Column(db.Text)
    jour = db.Column(db.Text)
    statut = db.Column(db.Text)
    user = db.relationship('User', backref='reserveur_mat', uselist=False)
    salle = db.Column(db.Text)

    def __init__(self, materiel, filiere, matiere, h_debut, h_fin, statut, salle, user):
        self.filiere = filiere
        self.matiere = matiere
        self.h_debut = h_debut
        self.h_fin = h_fin
        self.statut = statut
        self.materiel = materiel
        self.salle = salle
        self.user = user


class Historique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reserv_id = db.Column(db.Text)
    type = db.Column(db.Text)
    filiere = db.Column(db.Text)
    matiere = db.Column(db.Text)
    h_debut = db.Column(db.Text)
    h_fin = db.Column(db.Text)
    jour = db.Column(db.Text)
    statut = db.Column(db.Text)
    user = db.Column(db.Text)

    def __init__(self, reserv_id, type, filiere, matiere, h_debut, h_fin, jour,  statut, user):
        self.reserv_id = reserv_id
        self.type = type
        self.filiere = filiere
        self.matiere = matiere
        self.h_debut = h_debut
        self.h_fin = h_fin
        self.jour = jour
        self.statut = statut
        self.user = user

@login_manager.user_loader
def load_user(id):
    return Admin.query.get(id)


class Admin(db.Model, UserMixin):
    # Create a table in the db
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), index=True)
    password = db.Column(db.String(128))

    def __init__(self, username, email, password):
        self.username = username
        self.password = password
        self.email = email


class User(db.Model, UserMixin):
    # Create a table in the db
    __tablename__ = 'User'
    matricule = db.Column(db.String(13), primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    poste = db.Column(db.Text)
    reservMat_id = db.Column(db.Text, db.ForeignKey('ReservMateriel.id'))
    reservSal_id = db.Column(db.Integer, db.ForeignKey('ReservSalle.id'))

    def __init__(self, username, matricule, email, poste):
        self.username = username
        self.matricule = matricule
        self.email = email
        self.poste = poste

