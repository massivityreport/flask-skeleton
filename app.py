#! /usr/bin/env python

import json
import argparse


from flask import Flask
from flask import render_template, request, redirect, url_for, flash, abort
from flask import Response
from peewee import *
from flask.ext.security import Security, PeeweeUserDatastore, \
    UserMixin, RoleMixin, login_required

from model import db, User, Role, UserRoles
import filters
from forms import *

# Create app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config['DATABASE'] = {
    'name': 'app.db',
    'engine': 'peewee.SqliteDatabase',
}
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_PASSWORD_SALT'] = 'super-secret'

# Setup Flask-Security
user_datastore = PeeweeUserDatastore(db, User, Role, UserRoles)
security = Security(app, user_datastore)

# template filters
app.register_blueprint(filters.blueprint)

@app.route("/")
@login_required
def home():
    return render_template('home.html')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the web app')
    parser.add_argument('configuration_file', help='The JSON configuration file')
    args = parser.parse_args()

    # Go !
    app.config['UI'] = json.load(open(args.configuration_file))
    db.init(app.config['UI']['database'])
    app.run(host=app.config['UI']['host'], port=app.config['UI']['port'], debug=True)
