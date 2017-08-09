from datetime import datetime
from dateutil import parser as datetime_parser
from dateutil.tz import tzutc
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from . import db
from .exceptions import ValidationError
from .utils import split_url


class Organization(db.Model):
    __tablename__ = 'organization'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    type = db.Column(db.Integer)  # 1 Intl NGO | 2 Local NGO | 3 Business ORG
    email = db.Column(db.String(64), unique=True)
    phone = db.Column(db.String(30))
    address = db.Column(db.String(180))
    country = db.Column(db.String(120))
    date = db.Column(db.DateTime, default=datetime.utcnow())
    users = db.relationship('User', backref='organization', lazy='dynamic')
    project = db.relationship('Project', backref='organization', lazy='dynamic')

    def get_url(self):
        return url_for('api.get_organization', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'name': self.name,
            'type': self.type,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'country': self.country,
            'users_url': url_for('api.get_organization_users', id=self.id, _external=True)
        }

    def import_data(self, data):
        try:
            self.name = data['name'],
            self.type = data['type'],
            self.email = data['email'],
            self.phone = data['phone'],
            self.address = data['address'],
            self.country = data['country']
        except KeyError as e:
            raise ValidationError('Invalid organization: missing ' + e.args[0])
        return self


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(128))
    email = db.Column(db.String(60), unique=True)
    phone = db.Column(db.String(30), unique=True)
    type = db.Column(db.Integer) # 0 Super Admin | 1 Admin | 2 Agent | 3 Member
    date = db.Column(db.DateTime, default=datetime.utcnow())
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), index=True)
    project = db.relationship('Project', backref='users', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    def get_url(self):
        return url_for('api.get_user', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'date': self.date,
            'organization_url': self.organization.get_url()
        }

    def import_data(self, data):
        try:
            self.username = data['username'],
            self.name = data['name'],
            self.email = data['email'],
            self.phone = data['phone']
        except KeyError as e:
            raise ValidationError('Invalid order: missing ' + e.args[0])

        return self

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    start = db.Column(db.Date)
    end = db.Column(db.Date)
    budget = db.Column(db.Float)
    donor = db.Column(db.String(240))
    date = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), index=True)

    def get_url(self):
        return url_for('api.get_project', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'name': self.name,
            'start': self.start,
            'end': self.end,
            'budget': self.budget,
            'donor': self.donor,
            'date': self.date,
            'user_id': self.user_id,
            'organization_url': self.organization.get_url()
        }

    def import_data(self, data):
        try:
            self.name = data['name'],
            self.start = data['start'],
            self.end = data['end'],
            self.budget = data['budget'],
            self.donor = data['donor'],
            self.user_id = data['user_id']
        except KeyError as e:
            raise ValidationError('Invalid order: missing ' + e.args[0])
        return self


class ProjectInterventionArea(db.Model):
    __tablename__ = 'project_intervention_area'
    id = db.Column(db.Integer, primary_key=True)


