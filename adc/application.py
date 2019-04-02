"""
application.py
- creates a Flask app instance and registers the database object.
"""

import enum

from flask import Flask, Blueprint, jsonify, g
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../adc.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "desidragons"
db = SQLAlchemy(app)

api = Blueprint('api', __name__)

auth = HTTPBasicAuth()

# ---------------- Models -------------------- #

class UserType(enum.Enum):
    LTM = 1
    ACADEMIC = 2
    TUTOR = 3

class Semester(enum.Enum):
    ONE = 1
    TWO = 2
    BOTH = 3

class AssessmentFormat(enum.Enum):
    MOLE_QUIZ = 1
    ASSIGNMENT = 2
    PRESENTATION = 3
    FORMAL_EXAM = 4
    ASSESSED_LAB = 5
    GROUP_PROJECT = 6
    PORTFOLIO = 7

class User(db.Model):  
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    usertype = db.Column(db.Enum(UserType))
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False, default="$6$rounds=656000$Mekxk00d5L5we4/3$CwY2NGNDHX1Yt6khinGYUJm/I5s2.3bmjgMLmmsRIVzowR.LWPqIF2KrauyfjuzyWD2MrPToRVNHxYCZAPsFf1")

    def to_dict(self):
        return dict(id=self.id,
                    usertype=self.usertype,
                    email=self.email,
                    password=self.password)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired.
        except BadSignature:
            return None # invalid token.
        user = User.query.get(data['id'])
        return user

class Module(db.Model):  
    __tablename__ = "module"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    semester = db.Column(db.Enum(Semester))
    academic = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return dict(id=self.id,
                    code=self.code,
                    name=self.name,
                    semester=self.semester,
                    academic=self.academic)

class Assessment(db.Model):
    __tablename__ = "assessment"

    id = db.Column(db.Integer, primary_key=True)
    format = db.Column(db.Enum(AssessmentFormat), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    marks = db.Column(db.Float, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    submission_date = db.Column(db.DateTime, nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    module = db.relationship("Module", backref=db.backref("assessments", lazy=True))

# ---------------- Other -------------------- #

@auth.verify_password
def verify_password(email_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(email_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(email=email_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user # set global user.
    return True

# ---------------- Routes -------------------- #

@app.route('/api/hello')
@auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % g.user.name })

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })

@app.route('/api/401')
@auth.login_required
def send_401():
    return "Not authorized", 401

app.register_blueprint(api, url_prefix="/api")

if __name__ == '__main__':
    app.run(port=8081) # run the server.
