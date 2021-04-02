import json
import os
import re

from authlib.integrations.flask_client import OAuth
from flask import Flask, render_template, abort, url_for, redirect, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from jinja2 import TemplateNotFound
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from blizzard import form_url, get_bnet, get_avatar
from .config import *

# Flask APP Setup
app = Flask(__name__)
app.secret_key = os.urandom(16)

# Flask config setup
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = HEROKU_DATABASE_URI
# 'postgresql://postgres:cetmoe@localhost:5433/local_cetmoe'

# User session management
login_manager = LoginManager()
login_manager.init_app(app)

# OAuth Setup Blizzard
oauth = OAuth(app)
oauth.register(
    'blizzard',
    client_id=BLIZZ_CLIENT_ID,
    client_secret=BLIZZ_CLIENT_SECRET,
    authorize_url='https://eu.battle.net/oauth/authorize',
    access_token_url='https://eu.battle.net/oauth/token'
)
blizzard = oauth.blizzard

# OAuth setup WCL
oauth.register(
    'wcl',
    authorize_url='https://www.warcraftlogs.com/oauth/authorize',
    access_token_url='https://www.warcraftlogs.com/oauth/token',
    client_id=WCL_CLIENT_ID,
    client_secret=WCL_CLIENT_SECRET
)
wcl = oauth.wcl

db = SQLAlchemy(app)

# Database
from .models import User

db.create_all()
migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Routes
@app.route('/')
def home():
    try:
        return render_template('base.html')
    except TemplateNotFound:
        abort(404)


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return blizzard.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    token = blizzard.authorize_access_token()

    bnet = get_bnet('eu', blizzard)
    if bnet:
        user = User.query.get(bnet)
        if user:
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
        else:
            user = User(bnet)
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
    return redirect('/')


@app.route('/profile/')
def profile():
    return render_template('profile.html')


@app.route('/wcl')
def connect_wcl():
    redirect_uri = url_for('auth_wcl', _external=True)
    return wcl.authorize_redirect(redirect_uri)


@app.route('/authorize/wcl')
def auth_wcl():
    token = wcl.authorize_access_token()
    return redirect('/')

@app.route('/logout')
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect('/')
