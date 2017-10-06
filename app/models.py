from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from . import db
from .exceptions import ValidationError
from .utils import generate_code
from sqlalchemy import and_, func
import arrow


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
    saving_group = db.relationship('SavingGroup', backref='organization', lazy='dynamic')

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
            'projects_url': url_for('api.get_organization_projects', id=self.id, _external=True),
            'sg_url': url_for('api.get_organizations_sg', id=self.id, _external=True)
        }

    def export_member(self):
        return {
           'member_url': url_for('api.get_user_member', id=self.id, _external=True)
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
    secondary_phone = db.Column(db.String(30), unique=True, nullable=True)
    type = db.Column(db.Integer)  # 0 Super Admin | 1 Admin | 2 Agent | 3 Member | 4 developer account
    date = db.Column(db.DateTime, default=datetime.utcnow())
    birth_date = db.Column(db.Date)
    gender = db.Column(db.Integer)  # 0 Male # 1 Female
    education = db.Column(db.String(64))
    location = db.Column(db.String(128))
    first_login = db.Column(db.Integer, default=1)  # 1 never logged in # 0 already logged in
    confirmation_code = db.Column(db.String(12), default=generate_code())
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), index=True)
    project = db.relationship('Project', backref='users', lazy='dynamic')
    financial = db.relationship('UserFinDetails', backref='users', lazy='dynamic')
    project_agent = db.relationship('ProjectAgent', backref='users', lazy='dynamic')
    saving_group = db.relationship('SavingGroup', backref='users', lazy='dynamic')
    member = db.relationship('SavingGroupMember', backref='users', lazy='dynamic')

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


class SavingGroup(db.Model):
    __tablename__ = 'saving_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    creation_date = db.Column(db.Date)
    status = db.Column(db.Integer)  # 1 Graduated | 0 Supervised
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), index=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    village_id = db.Column(db.Integer, db.ForeignKey('village.id'), index=True)

    sg_financial = db.relationship('SavingGroupFinDetails', backref='saving_group', lazy='dynamic')
    sg_member = db.relationship('SavingGroupMember', backref='saving_group', lazy='dynamic')
    sg_wallet = db.relationship('SavingGroupWallet', backref='saving_group', lazy='dynamic')
    sg_cycle = db.relationship('SavingGroupCycle', backref='saving_group', lazy='dynamic')
    sg_fine = db.relationship('SavingGroupFines', backref='saving_group', lazy='dynamic')
    sg_shares = db.relationship('SavingGroupShares', backref='saving_group', lazy='dynamic')

    def get_url(self):
        return url_for('api.get_sg', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'id': self.id,
            'name': self.name,
            'creation_date': self.creation_date,
            'status': self.status,
            'location': self.village.export_data(),
            'members_url': url_for('api.get_sg_members', id=self.id, _external=True),
            'cycle_url': url_for('api.get_sg_cycle', id=self.id, _external=True),
            'wallet': url_for('api.get_sg_wallet', id=self.id, _external=True),
            'shares_url': url_for('api.get_sg_current_shares', id=self.id, _external=True),
            'fines_url': url_for('api.get_sg_current_fines', id=self.id, _external=True)
        }

    def import_data(self, data):
        try:
            self.name = data['name'],
            self.creation_date = datetime.strptime(data['creation_date'], "%Y-%m-%d").date()
            self.status = data['status'],
            self.organization_id = data['organization_id'],
            self.agent_id = data['agent_id'],
            self.village_id = data['village_id']
        except KeyError as e:
            raise ValidationError('Invalid order: missing ' + e.args[0])
        return self


class SavingGroupWallet(db.Model):
    __tablename__ = 'sg_wallet'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    saving_group_id = db.Column(db.Integer, db.ForeignKey('saving_group.id'), index=True, unique=True)

    member_transaction = db.relationship('SgMemberContributions', backref='sg_wallet', lazy='dynamic')
    member_loan = db.relationship('MemberLoan', backref='sg_wallet', lazy='dynamic')
    member_social = db.relationship('MemberSocialFund', backref='sg_wallet', lazy='dynamic')
    member_fine = db.relationship('MemberFine', backref='sg_wallet', lazy='dynamic')

    def get_url(self):
        return url_for('api.get_wallet', id=self.id, _external=True)

    def export_data(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'date': self.date,
            'sg_url': url_for('api.get_sg', id=self.saving_group_id, _external=True),
            'loan_url': url_for('api.get_wallet_loan', id=self.id, _external=True),
            'social_fund_debit_url': url_for('api.get_wallet_social_fund_debit', id=self.id, _external=True),
            'social_fund_credit_url': url_for('api.get_wallet_social_fund_credit', id=self.id, _external=True),
            'savings_url': url_for('api.get_wallet_savings', id=self.id, _external=True),
            'self_url': self.get_url()
        }

    def credit_wallet(self, amount):
        self.amount = self.amount + float(amount)
        return self

    def debit_wallet(self, amount):
        self.amount = self.amount + float(amount)
        return self

    @classmethod
    def wallet(cls, saving_group_id):
        return SavingGroupWallet.query. \
            filter(SavingGroupWallet.saving_group_id == saving_group_id).first()


class SgMemberContributions(db.Model):
    __tablename__ = 'sg_member_contributions'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    operator = db.Column(db.Integer)  # 1 MTN # 2 TIGO # 3 AIRTEL
    type = db.Column(db.Integer)  # 1 Saving # 2 Social Fund
    date = db.Column(db.DateTime, default=datetime.utcnow())
    sg_cycle_id = db.Column(db.Integer, db.ForeignKey('sg_cycle.id'), index=True)
    sg_member_id = db.Column(db.Integer, db.ForeignKey('sg_member.id'), index=True)
    sg_wallet_id = db.Column(db.Integer, db.ForeignKey('sg_wallet.id'), index=True)

    def get_url(self):
        return url_for('api.get_contribution', id=self.id, _external=True)

    def get_operator(self):
        operators = ['MTN', 'TIGO', 'AIRTEL']
        return operators[self.operator - 1]

    def export_data(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'operator': self.get_operator(),
            'type': "Saving" if self.type == 1 else "Social fund",
            'date': self.date
        }

    def import_data(self, data):
        try:
            self.amount = data['amount'],
            self.operator = data['operator'],
            self.type = data['type']
        except KeyError as e:
            raise ValidationError('Invalid SgMemberContributions ' + e.args[0])
        return self

    @classmethod
    def sum_savings(cls, member_id):
        return db.session.\
            query(func.sum(SgMemberContributions.amount).label('amount')). \
            filter(and_(SgMemberContributions.sg_member_id == member_id,
                        SgMemberContributions.type == 1)).first()

    @classmethod
    def sum_social_fund(cls, member_id):
        return db.session. \
            query(func.sum(SgMemberContributions.amount).label('amount')). \
            filter(and_(SgMemberContributions.sg_member_id == member_id,
                        SgMemberContributions.type == 2)).first()


class MemberLoan(db.Model):
    __tablename__ = 'member_loan'
    id = db.Column(db.Integer, primary_key=True)
    amount_loaned = db.Column(db.Float)
    request_date = db.Column(db.DateTime, default=datetime.utcnow())
    interest_rate = db.Column(db.Integer)
    initial_date_repayment = db.Column(db.Integer)
    date_payment = db.Column(db.DateTime)
    sg_cycle_id = db.Column(db.Integer, db.ForeignKey('sg_cycle.id'), index=True)
    sg_member_id = db.Column(db.Integer, db.ForeignKey('sg_member.id'), index=True)
    sg_wallet_id = db.Column(db.Integer, db.ForeignKey('sg_wallet.id'), index=True)

    approved = db.relationship('MemberApprovedLoan', backref='member_loan',  lazy='dynamic')

    def get_url(self):
        return url_for('api.get_loan', id=self.id, _external=True)

    def export_data(self):
        return {
            'id': self.id,
            'amount_loaned': self.amount_loaned,
            'date': self.request_date,
            'interest_rate': self.interest_rate,
            'date_repayment': self.initial_date_repayment,
            'expect_date_repayment': self.request_date + timedelta(days=self.initial_date_repayment)
        }

    def import_data(self, data):
        try:
            self.amount_loaned = data['amount_loaned'],
            self.interest_rate = data['interest_rate'],
            self.initial_date_repayment = data['initial_date_repayment']
        except KeyError as e:
            raise ValidationError('Invalid sg_debit_loan' + e.args[0])
        return self

    def date_rep(self):
        pass


class MemberApprovedLoan(db.Model):
    __tablename__ = 'member_approved_loan'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer)  # 1 Approved 0 Declined # 2 Pending
    date = db.Column(db.DateTime, default=datetime.utcnow())
    status_date = db.Column(db.DateTime)
    loan_id = db.Column(db.Integer, db.ForeignKey('member_loan.id'), index=True)
    sg_member_id = db.Column(db.Integer, db.ForeignKey('sg_member.id'), index=True)

    def get_url(self):
        return url_for('api.get_approved_loan', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'id': self.id,
            'status': self.status,
            'loan_url': url_for('api.get_loan', id=self.loan_id, _external=True),
            'sg_member_url': url_for('api.get_sg_member', id=self.sg_member_id, _external=True)
        }

    def import_data(self, data):
        try:
            self.status = data['status']
            self.sg_member_id = data['sg_member_id']
        except KeyError as e:
            ValidationError('Invalid sg approved loan' + e.args[0])
        return self

    def approve_loan(self):
        self.status = 1
        self.status_date = datetime.utcnow()
        return self

    def decline_loan(self):
        self.status = 0
        self.status_date = datetime.utcnow()
        return self


class MemberSocialFund(db.Model):
    __tablename__ = 'member_social_fund'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    sg_cycle_id = db.Column(db.Integer, db.ForeignKey('sg_cycle.id'), index=True)
    sg_member_id = db.Column(db.Integer, db.ForeignKey('sg_member.id'), index=True)
    sg_wallet_id = db.Column(db.Integer, db.ForeignKey('sg_wallet.id'), index=True)

    approved = db.relationship('MemberApprovedSocial', backref='member_social_fund', lazy='dynamic')

    def get_url(self):
        return url_for('api.get_social_fund', id=self.id, _external=True)

    def export_data(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'sg_cycle_id': self.sg_cycle_id,
            'sg_member_id': self.sg_member_id,
            'sg_wallet_id': self.sg_wallet_id
        }

    def import_data(self, data):
        try:
            self.amount = data['amount']
        except KeyError as e:
            ValidationError('Invalid Social Debit' + e.args[0])
        return self


class MemberApprovedSocial(db.Model):
    __tablename__ = 'member_approved_social'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer)  # 1 Approved 0 Declined # 2 Pending
    date = db.Column(db.DateTime, default=datetime.utcnow())
    status_date = db.Column(db.DateTime)
    social_debit_id = db.Column(db.Integer, db.ForeignKey('member_social_fund.id'), index=True)
    sg_member_id = db.Column(db.Integer, db.ForeignKey('sg_member.id'), index=True)

    def get_url(self):
        return url_for('api.get_approve_social_fund', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'id': self.id,
            'status': self.status,
            'social_fund_url': url_for('api.get_social_fund', id=self.social_debit_id, _external=True),
            'sg_member_url': url_for('api.get_sg_member', id=self.sg_member_id, _external=True)
        }

    def import_data(self, data):
        try:
            self.status = data['status']
            self.sg_member_id = data['sg_member_id']
        except KeyError as e:
            ValidationError('Invalid sg approved loan' + e.args[0])
        return self

    def approve_social(self):
        self.status = 1
        self.status_date = datetime.utcnow()
        return self

    def decline_social(self):
        self.status = 0
        self.status_date = datetime.utcnow()
        return self


class SavingGroupFines(db.Model):
    __tablename__ = 'sg_fines'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    social_fund = db.Column(db.Integer)
    attendance = db.Column(db.Integer)
    loan = db.Column(db.Integer)
    saving = db.Column(db.Integer)
    meeting = db.Column(db.Integer)
    saving_group_id = db.Column(db.Integer, db.ForeignKey('saving_group.id'), index=True)
    sg_cycle_id = db.Column(db.Integer, db.ForeignKey('sg_cycle.id'), index=True)
    db.Index('unique_fine', saving_group_id, sg_cycle_id, unique=True)

    def get_url(self):
        return url_for('api.get_sg_current_fines', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'id': self.id,
            'date': self.date,
            'social_fund_fine': self.social_fund,
            'attendance_fine': self.attendance,
            'loan_fine': self.loan,
            'saving_fine': self.saving,
            'meeting_absence': self.meeting
        }

    def import_data(self, data):
        try:
            self.social_fund = data['social_fund_fine']
            self.attendance = data['attendance_fine']
            self.loan = data['loan_fine']
            self.saving = data['saving_fine']
            self.meeting = data['meeting_absence']
        except KeyError as e:
            ValidationError('Invalid SavingGroupFines ' + e.args[0])
        return self


class SavingGroupShares(db.Model):
    __tablename__ = 'saving_group_shares'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    share = db.Column(db.Integer)
    interest_rate = db.Column(db.Integer)
    max_share = db.Column(db.Integer)
    social_fund = db.Column(db.Integer)
    saving_group_id = db.Column(db.Integer, db.ForeignKey('saving_group.id'), index=True)
    sg_cycle_id = db.Column(db.Integer, db.ForeignKey('sg_cycle.id'), index=True)
    db.Index('unique_share', saving_group_id, sg_cycle_id, unique=True)

    def get_url(self):
        return url_for('api.get_sg_current_shares', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'id': self.id,
            'date': self.date,
            'share': self.share,
            'interest_rate': self.interest_rate,
            'max_share': self.max_share,
            'social_fund': self.social_fund
        }

    def import_data(self, data):
        try:
            self.share = data['share'],
            self.interest_rate = data['interest_rate'],
            self.max_share = data['max_share'],
            self.social_fund = data['social_fund']
        except KeyError as e:
            ValidationError('Invalid SavingGroupShares' + e.args[0])
        return self


class MemberFine(db.Model):
    __tablename__ = 'member_fine'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, default=0)  # 1 Payed | 0 Not payed
    type = db.Column(db.String(20))  # 1 social_fund_fine | 2 loan_fine |
    # 3 meeting_absence | 4 saving_fine | attendance_fine
    amount = db.Column(db.Integer)
    initialization_date = db.Column(db.DateTime, default=datetime.utcnow())
    payment_date = db.Column(db.DateTime, nullable=True)
    initiate_by = db.Column(db.Integer)  # admin member
    member_id = db.Column(db.Integer, db.ForeignKey('sg_member.id'), index=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('sg_wallet.id'), index=True)
    cycle_id = db.Column(db.Integer, db.ForeignKey('sg_cycle.id'), index=True)

    def get_url(self):
        return url_for('api.get_fine', id=self.id, _external=True)

    def export_data(self):
        return {
            'id':self.id,
            'status': self.status,
            'type': self.type,
            'amount': self.amount,
            'initialization_date': self.initialization_date,
            'payment_date': self.payment_date,
            'self_url': self.get_url(),
            'initiator_url': url_for('api.get_sg_member', id=self.initiate_by, _external=True),
            'member_url': url_for('api.get_sg_member', id=self.member_id, _external=True)
        }

    def import_data(self, data):
        try:
            self.type = data['type']
            self.amount = data['amount']
            self.initiate_by = data['initiate_by']
        except KeyError as e:
            ValidationError('Invalid Member Fine ' + e.args[0])
        return self

    def repay_fine(self):
        self.status = 1
        self.payment_date = datetime.utcnow()
        return self


class SavingGroupCycle(db.Model):
    __tablename__ = 'sg_cycle'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Date)
    end = db.Column(db.Date)
    active = db.Column(db.Integer, default=1)  # 1 active cycle | 0 not actif cycle
    saving_group_id = db.Column(db.Integer, db.ForeignKey('saving_group.id'), index=True)
    drop_out = db.relationship('SavingGroupDropOut', backref='sg_cycle', lazy='dynamic')
    contributions = db.relationship('SgMemberContributions', backref='sg_cycle', lazy='dynamic')
    member_loan = db.relationship('MemberLoan', backref='sg_cycle', lazy='dynamic')
    member_social = db.relationship('MemberSocialFund', backref='sg_cycle', lazy='dynamic')
    member_fine = db.relationship('MemberFine', backref='sg_cycle', lazy='dynamic')
    sg_fines = db.relationship('SavingGroupFines', backref='sg_cycle', lazy='dynamic')
    sg_shares = db.relationship('SavingGroupShares', backref='sg_cycle', lazy='dynamic')
    db.Index('unique_cycle', start, end, saving_group_id, unique=True)

    def get_url(self):
        return url_for('api.get_cycle', id=self.id, _external=True)

    def export_data(self):
        return {
            'id': self.id,
            'start': self.start,
            'end': self.end,
            'active': self.active,
            'self_url': self.get_url(),
            'sg_url': url_for('api.get_sg', id=self.saving_group_id, _external=True),
            'loan_url': url_for('api.get_cycle_loan', id=self.id, _external=True),
            'social_fund_debit_url': url_for('api.get_cycle_social_fund_debit', id=self.id, _external=True),
            'social_fund_credit_url': url_for('api.get_cycle_social_fund_credit', id=self.id, _external=True),
            'savings_url': url_for('api.get_cycle_savings', id=self.id, _external=True),


        }

    def import_data(self, data):
        try:
            self.start = datetime.strptime(data['start'], "%Y-%m-%d").date(),
            self.end = datetime.strptime(data['end'], "%Y-%m-%d").date()
        except KeyError as e:
            raise ValidationError('Invalid Cycle ' + e.args[0])
        return self

    @classmethod
    def current_cycle(cls, saving_group_id):
        return SavingGroupCycle.query.\
            filter(and_(SavingGroupCycle.active == 1,
                        SavingGroupCycle.saving_group_id == saving_group_id)).first()


class SavingGroupMember(db.Model):
    __tablename__ = 'sg_member'
    id = db.Column(db.Integer, primary_key=True)
    saving_group_id = db.Column(db.Integer, db.ForeignKey('saving_group.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    pin = db.Column(db.String(128), index=True)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    admin = db.Column(db.Integer)  # 1 Admin # 0 Normal Member

    drop_out = db.relationship('SavingGroupDropOut', backref='sg_member', lazy='dynamic')
    member_loan = db.relationship('MemberLoan', backref='sg_member', lazy='dynamic')
    approved_loan = db.relationship('MemberApprovedLoan', backref='sg_member', lazy='dynamic')
    member_social = db.relationship('MemberSocialFund', backref='sg_member', lazy='dynamic')
    approve_social = db.relationship('MemberApprovedSocial', backref='sg_member', lazy='dynamic')
    member_fine = db.relationship('MemberFine', backref='sg_member', lazy='dynamic')
    member_contribution = db.relationship('SgMemberContributions', backref='sg_member', lazy='dynamic')
    member_mini_statement = db.relationship('MemberMiniStatement', backref='sg_member', lazy='dynamic')

    db.Index('member_sg_index', saving_group_id, user_id, unique=True)

    def set_pin(self, pin):
        self.pin = generate_password_hash(pin)

    def verify_pin(self, pin):
        return check_password_hash(self.pin, pin)

    def get_url(self):
        return url_for('api.get_sg_member', id=self.id, _external=True)

    def export_data(self):
        return {
            'id': self.id,
            'user_url': url_for('api.get_user', id=self.user_id, _external=True),
            'admin': self.admin,
            'date': self.date,
            'self_url': self.get_url(),
            'sg_url': url_for('api.get_sg', id=self.saving_group_id, _external=True),
            'approved_loan_url': url_for('api.get_member_approve_loan', id=self.id, _external=True),
            'pending_loan_url': url_for('api.get_member_pending_loan', id=self.id, _external=True),
            'approved_social_fund_url': url_for('api.get_member_approve_social_fund', id=self.id, _external=True),
            'pending_social_fund_url': url_for('api.get_member_pending_social_fund', id=self.id, _external=True),
            'member_fine': url_for('api.get_member_fine', id=self.id, _external=True)
        }

    def import_data(self, data):
        try:
            self.user_id = data['user_id']
            self.admin = data['admin']
        except KeyError as e:
            raise ValidationError('Invalid sg_member '+ e.args[0])
        return self

    @classmethod
    def group_admin(cls, saving_group_id):
        return SavingGroupMember.query.\
                filter(and_(SavingGroupMember.saving_group_id == saving_group_id, SavingGroupMember.admin == 1))


class MemberMiniStatement(db.Model):
    __tablename__ = 'members_mini_statement'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    type = db.Column(db.Integer)  # 1 Savings | 2 Social Fund | 3 Loan | 4 Debit Social Fund | 5 Fine
    date = db.Column(db.DateTime, default=datetime.utcnow())
    member_id = db.Column(db.Integer, db.ForeignKey('sg_member.id'), index=True)

    def get_url(self):
        return url_for('api.get_mini_statement', id=self.id, _external=True)

    def export_data(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'type': self.mini_statement_type(),
            'date': arrow.get(self.date).to('Africa/Kigali').humanize(),
            'member_id': self.member_id,
            'member_url': url_for('api.get_sg_member', id=self.member_id, _external=True),
            'statement': self.statement(),
            'self_url': self.get_url()
        }

    def import_data(self, data):
        try:
            self.amount = data['amount']
            self.type = data['type']
        except KeyError as e:
            raise ValidationError('Invalid MemberMiniStatement ' + e.args[0])
        return self

    def mini_statement_type(self):
        data = ['Savings', 'Social Fund', 'Loan', 'Debit Social Fund', 'Fine']
        return data[self.type - 1]

    def statement(self):
        date = arrow.get(self.date).to('Africa/Kigali').humanize()
        return '{} {} {}'.format(date, self.mini_statement_type(), self.amount)


class SavingGroupDropOut(db.Model):
    __tablename__ = 'sg_drop_out'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    sg_member_id = db.Column(db.Integer, db.ForeignKey('sg_member.id'), index=True)
    sg_cycle_id = db.Column(db.Integer, db.ForeignKey('sg_cycle.id'), index=True)

    def get_url(self):
        return url_for('api.get_sg_member_drop', id=self.id, _external=True)

    def export_data(self):
        return {
            'id': self.id,
            'date': self.date,
            'sg_member_id': self.sg_member_id
        }

    def import_data(self, data):
        try:
            pass
        except KeyError as e:
            raise ValidationError('invalid Drop dout ' + e.args[0])
        return self


class SavingGroupFinDetails(db.Model):
    __tablename__ = 'sg_fin_details'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    type = db.Column(db.Integer)  # 1 Banks # 2 MFIs # 3 Usacco # 4 NUsacco # 5 Telco
    account = db.Column(db.String(64))
    saving_group_id = db.Column(db.Integer, db.ForeignKey('saving_group.id'), index=True)

    def get_url(self):
        return url_for('api.get_sg_fin_details', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'name': self.name,
            'type': self.type,
            'account': self.account,
            'user_id': self.user_id
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
    partner_id = db.Column(db.Integer)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), index=True)
    intervention = db.relationship('InterventionArea', backref='project', lazy='dynamic')
    project_agent = db.relationship('ProjectAgent', backref='project', lazy='dynamic')
    saving_group = db.relationship('SavingGroup', backref='project', lazy='dynamic')

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
            'organization_url': self.organization.get_url(),
            'intervention_area_url': url_for('api.get_project_intervention_area', id=self.id, _external=True),
            'saving_groups_url': url_for('api.get_project_sgs', id=self.id, _external=True)

        }

    def import_data(self, data):
        try:
            self.name = data['name'],
            self.start = data['start'],
            self.end = data['end'],
            self.budget = data['budget'],
            self.donor = data['donor'],
            self.user_id = data['user_id'],
            self.partner_id = data['partner_id']

        except KeyError as e:
            raise ValidationError('Invalid order: missing ' + e.args[0])
        return self


class ProjectAgent(db.Model):
    __tablename__ = 'project_agent'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def get_url(self):
        return url_for('api.get_project_agent', id=self.id, _external=True)

    def export_data(self):
        return {
            'project': self.project.export_data(),
            'date': self.date
        }

    def import_data(self, data):
        try:
            self.user_id = data['user_id']
        except KeyError as e:
            raise ValidationError('Invalid ProjectAgent: missing ' + e.args[0])
        return self


class InterventionArea(db.Model):
    __tablename__ = 'intervention_area'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    village_id = db.Column(db.Integer, db.ForeignKey('village.id'), index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), index=True)

    def get_url(self):
        return url_for('api.get_intervention_area', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'date': self.date,
            'village': self.village.export_data()
        }

    def export_agent_project(self):
        return {
            'project': self.project.export_data()
        }

    def import_data(self, data):
        try:
            self.village_id = data['village_id']
        except KeyError as e:
            raise ValidationError('Invalid order: missing ' + e.args[0])
        return self


class Village(db.Model):
    __tablename__ = 'village'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    code = db.Column(db.String(20), unique=True)
    intervention = db.relationship('InterventionArea', backref='village', lazy='dynamic')
    saving_group = db.relationship('SavingGroup', backref='village', lazy='dynamic')

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
