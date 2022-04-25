from flask import Blueprint, render_template, session, redirect, url_for, flash
from projet import db
from projet.utilisateur.forms import ReservationForm, RechercheForm
from projet.BDonnees import ReservMateriel, ReservSalle, Materiel, Salle, User
import datetime

utilisateur_blueprint = Blueprint('utilisateur', __name__, template_folder='templates')


@utilisateur_blueprint.route('/list/<reserv_id>', methods=['GET', 'POST'])
def liste(reserv_id):
    # Grab a list of materials from database.
    form = RechercheForm()
    form1 = ReservationForm()

    try:
        user = User.query.filter_by(matricule=str(session['user'])).first()
    except:
        flash('Veuillez vous connecter pour pouvoir effectuer une reservation')
        return redirect(url_for('connexion'))

    if form1.submit1.data and form1.is_submitted():
        filiere = form1.filiere.data
        salle_filiere = form1.salle.data
        matiere = form1.matiere.data
        h_debut = form1.h_debut.data
        h_fin = form1.h_fin.data
        statut = 'EN ATTENTE'

        try:
            user = User.query.filter_by(matricule=str(session['user'])).first()
        except:
            flash('Veuillez vous connecter pour pouvoir effectuer une reservation')
            return redirect(url_for('connexion'))

        materiel = Materiel.query.filter_by(sn=reserv_id).first()
        salle = Salle.query.filter_by(id=reserv_id).first()


        if materiel is not None and materiel.reserv_id is None:
            user.reservMat_id = reserv_id
            materiel.reserv_id = reserv_id
            reserv = ReservMateriel(materiel, filiere, matiere, h_debut.strftime('%H:%M'), h_fin.strftime('%H:%M'), statut, salle_filiere, user)
            reserv.jour = datetime.date.today().strftime('%d-%b-%Y')
            db.session.add(reserv)
            db.session.commit()
            flash("Reservation de materiel effectué")
        elif salle is not None and salle.reserv_id is None:
            user.reservSal_id = reserv_id
            salle.reserv_id = reserv_id
            reserv = ReservSalle(salle, filiere, matiere, h_debut.strftime('%H:%M'), h_fin.strftime('%H:%M'), statut, user)
            reserv.jour = datetime.date.today().strftime('%d-%b-%Y')
            db.session.add(reserv)
            db.session.commit()
            flash("Reservation de salle effectué")
        else:
            flash("Materiel déja reservé, veuillez en choisir un autre")

        return redirect(url_for('utilisateur.liste', reserv_id=' '))

    if form.critere.data != '' and form.validate_on_submit():
        cri = form.critere.data
        form.critere.data = ''
        critere = cri.upper()
        materiel = Materiel.query.filter(((Materiel.type == critere) | (Materiel.model == critere) |
                                         (Materiel.exigence == critere) | (Materiel.sn == critere)) & (Materiel.reserv_id == None))
        salle = Salle.query.filter((Salle.type == critere) | (Salle.nbre_place == critere) & (Salle.reserv_id == None))
        user = User.query.filter_by(matricule=str(session['user'])).first()
        return render_template('reservation.html', materiel=materiel, salle=salle, form=form, form1=form1, user=user)
    else:
        materiel = Materiel.query.filter_by(reserv_id=None)
        salle = Salle.query.filter_by(reserv_id=None)

    user = User.query.filter_by(matricule=str(session['user'])).first()
    return render_template('reservation.html', materiel=materiel, salle=salle, form=form, form1=form1, user=user)

