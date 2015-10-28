#! /usr/bin/env python

import json
import argparse

from flask import Flask
from model import db, User, Role, UserRoles
from flask.ext.security import PeeweeUserDatastore

# Create app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config['DATABASE'] = {
    'name': 'app.db',
    'engine': 'peewee.SqliteDatabase',
}
user_datastore = PeeweeUserDatastore(db, User, Role, UserRoles)

def create_user():
    for Model in (Role, User, UserRoles):
        Model.drop_table(fail_silently=True)
        Model.create_table(fail_silently=True)
    user_datastore.create_user(email='scoupon', password='Phoenix85001')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the web ui')
    parser.add_argument('configuration_file', help='The JSON configuration file')
    args = parser.parse_args()

    # Go !
    app.config['UI'] = json.load(open(args.configuration_file))
    db.init(app.config['UI']['database'])
    create_user()
