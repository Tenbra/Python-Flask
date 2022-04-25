import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()
app = Flask(__name__)

# Configuration de l'appli
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Donnees.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'connexion'

# NOTE! These imports need to come after you've defined db, otherwise you will
# get errors in your models.py files.
# Grab the blueprints from the other views.py files for each "app"


from projet.utilisateur.pages import utilisateur_blueprint
from projet.administrateur.pages import administrateur_blueprint

app.register_blueprint(utilisateur_blueprint, url_prefix="/utilisateur")
app.register_blueprint(administrateur_blueprint, url_prefix='/administrateur')

