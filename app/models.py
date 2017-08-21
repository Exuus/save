from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from . import db
from .exceptions import ValidationError
from .utils import generate_code


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
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'country': self.country,
            'agents_url': url_for('api.get_organization_agents', id=self.id, _external=True),
            'members_url': url_for('api.get_organization_members', id=self.id, _external=True),
            'projects_url': url_for('api.get_organization_projects', id=self.id, _external=True)
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
    secondary_phone = db.Column(db.String(30), unique=True)
    type = db.Column(db.Integer) # 0 Super Admin | 1 Admin | 2 Agent | 3 Member | 4 developer account
    date = db.Column(db.DateTime, default=datetime.utcnow())
    birth_date = db.Column(db.Date)
    gender = db.Column(db.Integer)  # 0 Male # 1 Female
    education = db.Column(db.String(64))
    location = db.Column(db.String(128))
    first_login = db.Column(db.Integer, default=1)  # 1 never logged in # 0 already logged in
    confirmation_code = db.Column(db.String(12), default=generate_code())
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), index=True)
    project = db.relationship('Project', backref='users', lazy='dynamic')
    intervention = db.relationship('InterventionArea', backref='users', lazy='dynamic')
    financial = db.relationship('UserFinDetails', backref='users', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=86400):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    def get_url(self):
        return url_for('api.get_user', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'secondary_phone': self.phone,
            'date': self.date,
            'type': self.type,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'education': self.education,
            'first_login': self.first_login,
            'confirmation_code': self.confirmation_code,
            'projects_url': url_for('api.get_users_projects', id=self.id, _external=True),
            'financial_details': url_for('api.get_fin_details', id=self.id, _external=True)
        }

    def import_data(self, data):
        try:
            self.username = data['username'],
            self.name = data['name'],
            self.email = data['email'],
            self.phone = data['phone'],
            self.secondary_phone = data['secondary_phone'],
            self.type = data['type'],
            self.birth_date = datetime.strptime(data['birth_date'], "%Y-%m-%d").date(),
            self.gender = data['gender'],
            self.education = data['education']
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


class UserFinDetails(db.Model):
    __tablename = 'user_fin_details'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    type = db.Column(db.Integer)    # 1 Banks # 2 MFIs # 3 Usacco # NUsacco # Telco
    account = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)

    def get_url(self):
        return url_for('api.get_fin_details', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'name': self.name,
            'type': self.type,
            'account': self.account,
            'user_id':self.user_id
        }

    def import_data(self, data):
        try:
            self.name = data['name'],
            self.type = data['type'],
            self.account = data['account']
        except KeyError as e:
            raise ValidationError('Invalid financial: missing ' + e.args[0])
        return self


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
    intervention = db.relationship('InterventionArea', backref='project', lazy='dynamic')

    def get_url(self):
        return url_for('api.get_project', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'id': self.id,
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


class InterventionArea(db.Model):
    __tablename__ = 'intervention_area'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    village_id = db.Column(db.Integer, db.ForeignKey('village.id'), index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)

    def get_url(self):
        return url_for('api.get_intervention_area', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'date': self.date,
            'village': self.village.export_data(),
            'project': self.project.export_data(),
            'user_id': self.user_id
        }

    def import_data(self, data):
        try:
            self.village_id = data['village_id'],
            self.user_id = data['user_id'],
        except KeyError as e:
            raise ValidationError('Invalid order: missing ' + e.args[0])
        return self


class Village(db.Model):
    __tablename__ = 'village'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    code = db.Column(db.String(20), unique=True)
    intervention = db.relationship('InterventionArea', backref='village', lazy='dynamic')

    def get_url(self):
        return url_for('api.get_village', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url':self.get_url(),
            'name': self.name,
            'code': self.code
        }

    def import_data(self,data):
        try:
            self.name = data['name'],
            self.code = data['code'],
        except KeyError as e:
            raise ValidationError('Invalid order: missing ' + e.args[0])
        return self