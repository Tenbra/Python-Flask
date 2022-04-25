# This is app.py, this is the main file called.
from projet import app
from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, login_required, logout_user
from projet.BDonnees import User, Admin
from projet.forms import LoginForm


@app.route('/', methods=['GET', 'POST'])
def connexion():
    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user and admin from our Models table
        admin = Admin.query.filter_by(email=form.email.data).first()
        user = User.query.filter_by(email=form.email.data).first()
        password = form.password.data

        if admin is not None and user is None:
            if admin.password == password:
                # Log in the admin
                login_user(admin)
                session['admin'] = admin.email
                next = request.args.get('next')
                if next == None or next[0] == '/':
                    next = url_for('administrateur.accueil')
                return redirect(next)
            else:
                flash('Mot de passe incorrect!')
                form.email.data = admin.email
                render_template('home.html', form=form)

        elif user is not None and admin is None:
            if user.matricule == password:
                # Log in the user
                session['user'] = user.matricule
                next = url_for('utilisateur.liste', reserv_id=' ')
                return redirect(next)
            else:
                flash('Mot de passe incorrect!')
                form.email.data = user.email
                render_template('home.html', form=form)
        else:
            flash('Email non reconnu dans la base de données')

    return render_template('home.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous vous etes deconnecté!')
    return redirect(url_for('connexion'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
