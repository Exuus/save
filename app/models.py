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
    date = db.Column(db.DateTime, default=datetime.now)
    users = db.relationship('User', backref='organization', lazy='dynamic')

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
            'country': self.country
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
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(128))
    email = db.Column(db.String(60))
    phone = db.Column(db.String(30))
    date = db.Column(db.DateTime, default=datetime.now)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), index=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def get_url(self):
        return url_for('api.get_organization', id=self.id, _external=True)

    def export_data(self):
        return {
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'date': self.date.isoformat(),
            'organization_url': self.customer.get_url()
        }

    def import_data(self, data):
        try:
            self.username = data['username'],
            self.name = data['name'],
            self.password_hash = self.set_password(data['passowrd']),
            self.email = self.email,
            self.phone = self.phone
        except KeyError as e:
            raise ValidationError('Invalid order: missing ' + e.args[0])

        return self