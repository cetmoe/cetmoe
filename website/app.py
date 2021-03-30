import os
from flask import Flask, render_template, abort, url_for, redirect, session
from authlib.integrations.flask_client import OAuth
from .config import BLIZZ_CLIENT_ID, BLIZZ_CLIENT_SECRET
from jinja2 import TemplateNotFound

app = Flask(__name__)
app.secret_key = os.urandom(16)
oauth = OAuth(app)

oauth.register(
    'blizzard',
    client_id=BLIZZ_CLIENT_ID,
    client_secret=BLIZZ_CLIENT_SECRET,
    authorize_url='https://eu.battle.net/oauth/authorize',
    access_token_url='https://eu.battle.net/oauth/token',
    api_base_url='eu.battle.net/'
)

blizzard = oauth.blizzard


@app.route('/')
def home():
    if 'token' in session:
        print(session['token'])
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return blizzard.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    token = blizzard.authorize_access_token()

    session['token'] = token

    # you can save the token into database
    profile = blizzard.get('https://eu.api.blizzard.com/profile/user/wow', token=token)
    return redirect('/')


@app.route('/profile')
def profile():
    return 'profile'
