from flask import Blueprint, render_template, redirect, url_for, flash, session
from projet import db
from flask_login import login_required
from projet.administrateur.forms import AddSalleForm, AddMaterielForm, RechercheForm, ResetForm, NewAdminForm,\
    NewUserForm
from projet.BDonnees import Materiel, Salle, ReservMateriel, ReservSalle, Admin, Historique, User, HistoriqueMS

administrateur_blueprint = Blueprint('administrateur', __name__, template_folder='templates')


@administrateur_blueprint.route('/add_materiel/<sn>', methods=['GET', 'POST'])
@login_required
def add_materiel(sn):
    form = AddMaterielForm()
    form1 = ResetForm()

    if sn is not None:
        materiel = Materiel.query.filter_by(sn=sn).first()

    if form.submit.data and form.validate_on_submit():
        type_mat = form.type_mat.data
        model = form.model.data
        exigence = form.exigence.data
        nserie = form.sn.data
        hidde = sn

        if hidde != ' ':
            # Modify existing material
            mat = Materiel.query.filter_by(sn=hidde).first()
            mat.type_mat = type_mat.upper()
            mat.model = model.upper()
            mat.exigence = exigence.upper()
            hist = HistoriqueMS(type_mat, sn, model, exigence, 'MODIFIE')
            flash('Materiel modifié')

        else:
            # Add new material to database
            mat = Materiel(nserie.upper(), type_mat.upper(), model.upper(), exigence.upper())
            hist = HistoriqueMS(mat.type, mat.sn, mat.model, mat.exigence, 'NOUVEAU')
            flash('Materiel ajouté')

        db.session.add(hist)
        db.session.add(mat)
        db.session.commit()
        return redirect(url_for('administrateur.liste', del_id=' '))

    elif form1.validate_on_submit() and form1.reset.data:
        form.type_mat.data = ''
        form.model.data = ''
        form.exigence.data = ''
        form.sn.data = ''

    return render_template('add_modif_materiel.html', form=form, form1=form1, materiel=materiel)


@administrateur_blueprint.route('/add_salle/<id>', methods=['GET', 'POST'])
@login_required
def add_salle(id):
    form = AddSalleForm()
    form1 = ResetForm()

    if id is not None:
        salle = Salle.query.filter_by(id=id).first()

    if form.submit.data and form.validate_on_submit():
        type_sal = form.type_sal.data
        numero = form.numero.data
        nbre_place = form.nbre_place.data
        hidde = id

        if hidde != ' ':
            sal = Salle.query.filter_by(id=hidde).first()
            sal.type_sal = type_sal.upper()
            sal.numero = numero.upper()
            sal.nbre_place = nbre_place.upper()
            db.session.add(sal)
            hist = HistoriqueMS(type_sal, sal.id, numero, nbre_place, 'MODIFIE')
            db.session.add(hist)
            db.session.commit()
            flash('Salle modifié')

        else:
            # Add new salle to database
            sal = Salle(type_sal.upper(), numero.upper(), nbre_place.upper())
            db.session.add(sal)
            db.session.commit()
            hist = HistoriqueMS(sal.type, sal.id, sal.numero, sal.nbre_place, 'NOUVEAU')
            db.session.add(hist)
            db.session.commit()
            flash('Salle ajouté')


        db.session.commit()

        return redirect(url_for('administrateur.liste', del_id=' '))

    elif form1.validate_on_submit() and form1.reset.data:
        form.type_sal.data = ''
        form.numero.data = ''
        form.nbre_place.data = ''

    return render_template('add_modif_salle.html', form=form, salle=salle, form1=form1)


@administrateur_blueprint.route('/liste/<del_id>', methods=['GET', 'POST'])
@login_required
def liste(del_id):

    if del_id != ' ':

        materiel = Materiel.query.filter_by(sn=del_id).first()
        salle = Salle.query.filter_by(id=del_id).first()

        if materiel is not None:
            hist = HistoriqueMS(materiel.type, materiel.sn, materiel.model, materiel.exigence, 'SUPPRIME')
            db.session.delete(materiel)
        else:
            hist = HistoriqueMS(salle.type, salle.id, salle.numero, salle.nbre_place, 'SUPPRIME')
            db.session.delete(salle)
        db.session.add(hist)
        db.session.commit()
        return redirect(url_for('administrateur.liste', del_id=' '))

    form = RechercheForm()
    if form.validate_on_submit() and form.cri.data != '':
        cri = form.cri.data
        form.cri.data = ''
        critere = cri.upper()
        materiels = Materiel.query.filter((Materiel.type == critere) | (Materiel.model == critere) |
                                          (Materiel.exigence == critere) | (Materiel.sn == critere))
        salles = Salle.query.filter((Salle.type == critere) | (Salle.nbre_place == critere))
    else:
        materiels = Materiel.query.all()
        salles = Salle.query.all()

    return render_template('liste.html', materiels=materiels, salles=salles, form=form)


@administrateur_blueprint.route('/compte/historique_materiaux_salle', methods=['GET'])
@login_required
def historique_materiaux_salle():
    hist = HistoriqueMS.query.order_by(HistoriqueMS.uniq_id)
    return render_template('historique_materiaux_salles.html', hist=hist)


@administrateur_blueprint.route('/accueil', methods=['GET', 'POST'])
@login_required
def accueil():
    r_salle = ReservSalle.query.filter_by(statut='EN COURS')
    r_materiel = ReservMateriel.query.filter_by(statut='EN COURS')
    return render_template('accueil.html', salles=r_salle, materiels=r_materiel)


@administrateur_blueprint.route('/confirm_mat/<confirm_id>', methods=['GET', 'POST'])
@login_required
def confirm_materiel(confirm_id):
    mat = ReservMateriel.query.filter_by(id=confirm_id).first()
    hist_mat = Historique(mat.materiel.sn, mat.materiel.type, mat.filiere, mat.matiere, mat.h_debut, mat.h_fin,
                          mat.jour, 'RENDUE', mat.user.username)
    db.session.delete(mat)
    db.session.add(hist_mat)
    db.session.commit()
    return redirect(url_for('administrateur.accueil'))


@administrateur_blueprint.route('/confirm_sal/<confirm_id>', methods=['GET', 'POST'])
@login_required
def confirm_salle(confirm_id):
    sal = ReservSalle.query.filter_by(id=confirm_id).first()
    hist_sal = Historique(sal.salle.id, sal.salle.type, sal.filiere, sal.matiere, sal.h_debut, sal.h_fin, sal.jour,
                          'LIBERE', sal.user.username)
    db.session.delete(sal)
    db.session.add(hist_sal)
    db.session.commit()
    return redirect(url_for('administrateur.accueil'))


@administrateur_blueprint.route('/demande/<demand_id>', methods=['GET', 'POST'])
@login_required
def demande(demand_id):

    if demand_id != ' ':
        dem_mat = ReservMateriel.query.filter_by(id=demand_id).first()
        dem_sal = ReservSalle.query.filter_by(id=demand_id).first()

        if dem_mat is not None:
            dem_mat.statut = 'EN COURS'
            db.session.add(dem_mat)
            db.session.commit()
            return redirect(url_for('administrateur.demande', demand_id=' '))
        else:
            dem_sal.statut = 'EN COURS'
            db.session.add(dem_sal)
            db.session.commit()
            return redirect(url_for('administrateur.demande', demand_id=' '))

    d_salle = ReservSalle.query.filter_by(statut='EN ATTENTE')
    d_materiel = ReservMateriel.query.filter_by(statut='EN ATTENTE')
    return render_template('demande.html', salles=d_salle, materiels=d_materiel)


@administrateur_blueprint.route('/supprim_mat/<confirm_id>', methods=['GET', 'POST'])
@login_required
def supprim_demand_materiel(confirm_id):
    mat = ReservMateriel.query.filter_by(id=confirm_id).first()
    hist_mat = Historique(mat.materiel.sn, mat.materiel.type, mat.filiere, mat.matiere, mat.h_debut, mat.h_fin,
                          mat.jour, 'SUPPRIME', mat.user.username)
    db.session.delete(mat)
    db.session.add(hist_mat)
    db.session.commit()
    return redirect(url_for('administrateur.accueil'))


@administrateur_blueprint.route('/supprim_sal/<confirm_id>', methods=['GET', 'POST'])
@login_required
def supprim_demand_salle(confirm_id):
    sal = ReservSalle.query.filter_by(id=confirm_id).first()
    hist_sal = Historique(sal.salle.id, sal.salle.type, sal.filiere, sal.matiere, sal.h_debut, sal.h_fin, sal.jour,
                          'SUPPRIME', sal.user.username)
    db.session.delete(sal)
    db.session.add(hist_sal)
    db.session.commit()
    return redirect(url_for('administrateur.accueil'))


@administrateur_blueprint.route('/compte', methods=['GET', 'POST'])
@login_required
def compte():
    admin = Admin.query.filter_by(email=session['admin']).first()

    form = NewAdminForm()
    if form.validate_on_submit():
        new_admin = Admin(username=form.nom.data, email=form.email.data, password=form.password.data)
        db.session.add(new_admin)
        db.session.commit()
        flash('Nouvel admin crée!')

    return render_template('compte.html', admin=admin, form=form)


@administrateur_blueprint.route('/compte/historique', methods=['GET'])
@login_required
def historique_reservation():
    hist = Historique.query.all()
    return render_template('historique_reservation.html', hist=hist)


@administrateur_blueprint.route('/utilisateur/<del_mat>', methods=['GET', 'POST'])
@login_required
def utilisateur(del_mat):
    if del_mat != ' ':
        del_user = User.query.filter_by(matricule=del_mat).first()
        db.session.delete(del_user)
        db.session.commit()
        flash('Utilisateur supprimé!')

    form1 = NewUserForm()
    if form1.validate_on_submit() and form1.submit.data:
        username = form1.username.data
        email = form1.email.data
        matricule = form1.matricule.data
        poste = form1.poste.data
        user = User.query.filter_by(matricule=matricule).first()
        if user is not None:
            user.matricule = matricule
            user.username = username.upper()
            user.email = email
            user.poste = poste
            db.session.add(user)
            flash('Utilisateur modifié !')
        else:
            new_user = User(username.upper(), matricule, email, poste)
            db.session.add(new_user)
            flash('Nouvel utilisateur crée !')
        db.session.commit()


    form = RechercheForm()
    if form.validate_on_submit() and form.cri.data != '':
        cri = form.cri.data
        form.cri.data = ''
        critere = cri.upper()
        users = User.query.filter((User.username == critere) | (User.matricule == critere) |
                                          (User.email == critere) | (User.poste == critere))
    else:
        users = User.query.all()

    return render_template('utilisateur.html', users=users, form=form, form1=form1)
