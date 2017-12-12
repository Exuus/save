from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import JSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from . import db
from .exceptions import ValidationError
from .utils import generate_code, generate_username, generate_email, monthdelta
from sqlalchemy import and_, func
import arrow
from decorators import paginate


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
    project_partner = db.relationship('ProjectPartner', backref='organization', lazy='dynamic')

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
    username = db.Column(db.String(64), index=True, unique=True, nullable=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(128))
    email = db.Column(db.String(60), unique=True)
    phone = db.Column(db.String(30), unique=True, index=True)
    type = db.Column(db.Integer)  # 0 Super Admin | 1 Admin | 2 Agent | 3 Member | 4 developer account
    date = db.Column(db.DateTime, default=datetime.utcnow())
    birth_date = db.Column(db.Date)
    gender = db.Column(db.Integer)  # 0 Male # 1 Female
    key = db.Column(db.String(64))
    education = db.Column(db.String(64), nullable=True)
    id_number = db.Column(db.String(60), unique=True, nullable=True)
    location = db.Column(db.String(128), default='no location')
    first_login = db.Column(db.Integer, default=1)  # 1 never logged in # 0 already logged in
    confirmation_code = db.Column(db.String(12), default=generate_code())
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), index=True)
    partner_id = db.Column(db.Integer, index=True)
    project = db.relationship('Project', backref='users', lazy='dynamic')
    financial = db.relationship('UserFinDetails', backref='users', lazy='dynamic')
    project_agent = db.relationship('ProjectAgent', backref='users', lazy='dynamic')
    saving_group = db.relationship('SavingGroup', backref='users', lazy='dynamic')
    member = db.relationship('SavingGroupMember', backref='users', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'id': self.id}).decode('utf-8')

    def reset_key(self):
        self.key = None
        return self

    def generate_sms_key(self):
        self.key = generate_code()
        return self.key

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
            'date': self.date,
            'type': self.type,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'education': self.education,
            'first_login': self.first_login,
            'id_number': self.id_number,
            'location': self.location,
            'confirmation_code': self.confirmation_code,
            'organization': self.organization.export_data(),
            'sg_url': url_for('api.get_agent_sg', id=self.id, _external=True),
            'projects_url': url_for('api.get_users_projects', id=self.id, _external=True),
            'financial_details': url_for('api.get_fin_details', id=self.id, _external=True)
        }

    def import_data(self, data):
        try:
            self.username = data['username']
            if data['username'] is None:
                self.username = generate_username(data['name'])
            self.name = data['name']

            self.email = data['email']
            if data['email'] is None:
                self.email = generate_email(data['name'])

            self.phone = data['phone']
            self.type = data['type']
            self.birth_date = datetime.strptime(data['birth_date'], "%Y-%m-%d").date()
            self.gender = data['gender']
            self.education = data['education']
            if self.education is None:
                self.education = None
            self.id_number = data['id_number']
            self.location = data['location']
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
    date = db.Column(db.DateTime, default=datetime.utcnow())
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
    sg_meeting = db.relationship('SavingGroupMeeting', backref='saving_group', lazy='dynamic')

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
            'agent_id': self.agent_id,
            'agent': self.users.export_data(),
            'members_url': url_for('api.get_sg_members', id=self.id, _external=True),
            'cycle_url': url_for('api.get_sg_cycle', id=self.id, _external=True),
            'wallet': url_for('api.get_sg_wallet', id=self.id, _external=True),
            'shares_url': url_for('api.get_sg_current_shares', id=self.id, _external=True),
            'fines_url': url_for('api.get_sg_current_fines', id=self.id, _external=True),
            'meetings_url': url_for('api.get_sg_meetings', id=self.id, _external=True),
            'organization_id': self.organization_id,
            'project_url': url_for('api.get_project', id=self.project_id, _external=True)
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

    @classmethod
    def project_agent_sg(cls, project_id):
        return db.session.query(func.count(SavingGroup.id).label('sg_count'),
                                User.name.label('user_name'), User.id.label('agent_id'),
                                SavingGroup.village_id, Project.name.label('project_name'),
                                Project.id.label('id'))\
            .join(User)\
            .filter(User.id == SavingGroup.agent_id)\
            .join(Project)\
            .filter(SavingGroup.project_id == Project.id)\
            .filter(Project.id == project_id)\
            .group_by(User.name, User.id, SavingGroup.village_id, Project.name, Project.id)


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
        self.amount = self.amount - float(amount)
        return self

    @classmethod
    def wallet(cls, saving_group_id):
        return SavingGroupWallet.query. \
            filter(SavingGroupWallet.saving_group_id == saving_group_id).first()

    def balance(self):
        return self.amount

    def share_out(self, shared_amount):
        balance = float(self.amount) - float(shared_amount)
        return {
            'reinvested_amount': balance,
            'shared_amount': shared_amount
        }


class SavingGroupShareOut(db.Model):
    __tablename__ = 'sg_share_out'
    id = db.Column(db.Integer, primary_key=True)
    shared_amount = db.Column(db.Float)
    reinvested_amount = db.Column(db.Float)
    cycle_id = db.Column(db.Integer, db.ForeignKey('sg_cycle.id'), index=True)

    def get_url(self):
        return url_for('api.get_share_out', id=self.id, _external=True)

    def export_data(self):
        return {
            'id': self.id,
            'shared_amount': self.shared_amount,
            'reinvested_amount': self.reinvested_amount,
            'cycle_id': self.cycle_id
        }

    def import_data(self, data):
        try:
            self.shared_amount = data['shared_amount']
            self.reinvested_amount = data['reinvested_amount']
        except KeyError as e:
            raise ValidationError('Invalid SG Share Out ' + e.args[0])
        return self


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
    def total_savings(cls, sg_id):
        cycle = SavingGroupCycle.current_cycle(sg_id)
        savings = db.session\
            .query(func.sum(SgMemberContributions.amount).label('savings'))\
            .join(SavingGroupMember)\
            .filter(SgMemberContributions.sg_member_id == SavingGroupMember.id)\
            .join(SavingGroup)\
            .filter(SavingGroup.id == SavingGroupMember.saving_group_id)\
            .filter(SavingGroup.id == sg_id) \
            .join(SavingGroupCycle) \
            .filter(SavingGroupCycle.id == SgMemberContributions.sg_cycle_id) \
            .filter(SavingGroupCycle.id == cycle.id) \
            .first()[0]
        return savings

    @classmethod
    def sum_social_fund(cls, member_id):
        return db.session. \
            query(func.sum(SgMemberContributions.amount).label('amount')). \
            filter(and_(SgMemberContributions.sg_member_id == member_id,
                        SgMemberContributions.type == 2)).first()

    @classmethod
    def member_savings(cls, sg_id):
        cycle = SavingGroupCycle.current_cycle(sg_id)
        return db.session\
            .query(func.sum(SgMemberContributions.amount).label('saving'), SgMemberContributions.sg_member_id)\
            .filter(SgMemberContributions.type == 1)\
            .join(SavingGroupMember)\
            .filter(SavingGroupMember.id == SgMemberContributions.sg_member_id)\
            .filter(SavingGroupMember.activate == 1)\
            .join(SavingGroup)\
            .filter(SavingGroup.id == SavingGroupMember.saving_group_id)\
            .filter(SavingGroup.id == sg_id) \
            .join(SavingGroupCycle) \
            .filter(SavingGroupCycle.id == SgMemberContributions.sg_cycle_id) \
            .filter(SavingGroupCycle.id == cycle.id) \
            .group_by(SgMemberContributions.sg_member_id)\
            .all()


class MemberLoan(db.Model):
    __tablename__ = 'member_loan'
    id = db.Column(db.Integer, primary_key=True)
    amount_loaned = db.Column(db.Float)
    request_date = db.Column(db.DateTime, default=datetime.utcnow())
    interest_rate = db.Column(db.Integer)
    initial_date_repayment = db.Column(db.Integer)
    date_payment = db.Column(db.DateTime)
    payment_type = db.Column(db.Integer)  # 0 Write-off | 1 Self-payed
    write_off_admin = db.Column(db.Integer)
    sg_cycle_id = db.Column(db.Integer, db.ForeignKey('sg_cycle.id'), index=True)
    sg_member_id = db.Column(db.Integer, db.ForeignKey('sg_member.id'), index=True)
    sg_wallet_id = db.Column(db.Integer, db.ForeignKey('sg_wallet.id'), index=True)

    approved = db.relationship('MemberApprovedLoan', backref='member_loan',  lazy='dynamic')
    loan_repayment = db.relationship('MemberLoanRepayment', backref='member_loan', lazy='dynamic')

    def get_url(self):
        return url_for('api.get_loan', id=self.id, _external=True)

    def export_data(self):
        return {
            'id': self.id,
            'amount_loaned': self.amount_loaned,
            'date': self.request_date,
            'interest_rate': self.interest_rate,
            'date_repayment': self.initial_date_repayment,
            'request_date': self.request_date,
            'expect_date_repayment': self.request_date + timedelta(days=self.initial_date_repayment),
            'sg_member_url': url_for('api.get_sg_member', id=self.sg_member_id, _external=True)
        }

    def import_data(self, data):
        try:
            self.amount_loaned = data['amount_loaned'],
            self.interest_rate = data['interest_rate'],
            self.initial_date_repayment = data['initial_date_repayment']
        except KeyError as e:
            raise ValidationError('Invalid sg_debit_loan' + e.args[0])
        return self

    def date_repayment(self):
        self.date_payment = datetime.utcnow()
        self.payment_type = 1

    def write_off(self, admin_id):
        self.date_payment = datetime.utcnow()
        self.payment_type = 0
        self.write_off_admin = admin_id

    @classmethod
    def get_loan_balance(cls, loan):
        loan_payed = MemberLoanRepayment.loan_payed(loan.id)[0]
        fine = loan.calculate_fine()
        loan_payed = 0 if loan_payed is None else loan_payed
        interest = loan.amount_loaned * loan.interest_rate / 100
        initial_loan_interest = float(interest + loan.amount_loaned)
        total_to_pay = float(interest + loan.amount_loaned + fine['amount'])
        remain = total_to_pay - float(loan_payed)
        return {
            'status': loan.get_payment_status(remain),
            'remain_amount': remain,
            'payed_amount': loan_payed,
            'initial_loan': loan.amount_loaned,
            'loan_interest': interest,
            'id': loan.id,
            'interest_rate': loan.interest_rate,
            'date_payment': loan.date_payment,
            'payment_type': loan.write_of_or_self_payed(),
            'request_date': loan.request_date,
            'initial_loan_plus_interest': initial_loan_interest,
            'total_loan_interest_plus_fine': total_to_pay,
            'fine': loan.calculate_fine(),
            'expect_date_repayment': loan.request_date + timedelta(days=loan.initial_date_repayment),
            "wallet_id": loan.sg_wallet_id,
            'amount_loaned': loan.amount_loaned
        }

    def get_payment_status(self, remain):
        if self.payment_type == 0:
            return 'payed'
        elif remain == 0:
            return 'payed'
        return 'not payed'

    def write_of_or_self_payed(self):
        if self.payment_type == 0:
            return 'write-off'
        return 'self-payed'

    @classmethod
    def post_loan(cls, member, data_json, admins):
        wallet = SavingGroupWallet.query. \
            filter(SavingGroupWallet.saving_group_id == member.saving_group_id).first()
        cycle = SavingGroupCycle.current_cycle(member.saving_group_id)

        loan = MemberLoan(
            sg_cycle=cycle,
            sg_wallet=wallet,
            sg_member=member
        )

        loan.import_data(data_json)
        db.session.add(loan)
        db.session.commit()

        """ add member approve Request """

        for admin in admins:
            data = dict()
            data['status'] = 2
            data['sg_member_id'] = admin.export_data()['id']
            approved_loan = MemberApprovedLoan(member_loan=loan)
            approved_loan.import_data(data)
            db.session.add(approved_loan)
            db.session.commit()
        return cls

    def calculate_fine(self):
        repayment_date = self.request_date + timedelta(days=self.initial_date_repayment)
        interest = self.amount_loaned * self.interest_rate / 100
        fine_rate = interest/self.initial_date_repayment

        if (datetime.now() > repayment_date) & (self.date_payment is None):
            days = (datetime.now() - repayment_date).days
            fine = days * fine_rate
            return {
                'amount': fine,
                'delays': days
            }
        elif (datetime.now() <= repayment_date) & (self.date_payment is None):
            return {
                'amount': 0,
                'delays': 0
            }
        elif (self.date_payment is not None) & (datetime.now() <= repayment_date):

            return {
                'amount': 0,
                'delays': 0
            }

        days = (self.date_payment - repayment_date).days
        fine = days * fine_rate
        return {
            'amount': fine,
            'delays': days
        }

    @classmethod
    def loan_status(cls, loan_id, saving_group_id):
        admins = SavingGroupMember.count_group_admin(saving_group_id)[0]
        loan_approved = MemberApprovedLoan.get_approved_loan(loan_id)[0]

        if admins == loan_approved:
            return True
        return False


class MemberLoanRepayment(db.Model):
    __table_name__ = 'member_loan_repayment'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    loan_id = db.Column(db.Integer, db.ForeignKey('member_loan.id'), index=True)

    def get_url(self):
        return url_for('api.loan_repayed', id=self.id, _external=True)

    def export_data(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'date': self.date,
            'loan_url': url_for('api.get_loan', id=self.loan_id, _external=True)
        }

    def import_data(self, data):
        try:
            self.amount = data['amount']
        except KeyError as e:
            raise ValidationError('Invalid Member Loan Repay' + e.args)
        return self

    @classmethod
    def loan_payed(cls, loan_id):
        return db.session.query(func.sum(MemberLoanRepayment.amount).label('loan_payed'))\
            .join(MemberLoan)\
            .filter(MemberLoan.id == MemberLoanRepayment.loan_id)\
            .filter(MemberLoan.id == loan_id).first()


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
            'date': self.date,
            'loan_url': url_for('api.get_loan', id=self.loan_id, _external=True),
            'sg_admin_url': url_for('api.get_sg_member', id=self.sg_member_id, _external=True)
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

    @classmethod
    def get_approved_loan(cls, loan_id):
        return db.session.query(func.count(MemberApprovedLoan.id)). \
            filter(and_(MemberApprovedLoan.loan_id == loan_id,
                        MemberApprovedLoan.status == 1)).first()


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
            'date': self.date,
            'sg_cycle_id': self.sg_cycle_id,
            'sg_member_id': self.sg_member_id,
            'sg_wallet_id': self.sg_wallet_id,
            'member_url': url_for('api.get_sg_member', id=self.sg_member_id, _external=True)
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
            'date': self.date,
            'social_fund_url': url_for('api.get_social_fund', id=self.social_debit_id, _external=True),
            'sg_admin_url': url_for('api.get_sg_member', id=self.sg_member_id, _external=True)
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

    @classmethod
    def get_approved_social_fund(cls, social_debit_id):
        return db.session.query(func.count(MemberApprovedSocial.id)).\
            filter(and_(MemberApprovedSocial.social_debit_id == social_debit_id,
                        MemberApprovedSocial.status == 1)).first()


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

    @classmethod
    def calculate_shares(cls, saving, sg_id):
        cycle = SavingGroupCycle.current_cycle(sg_id)
        shares = db.session.query(SavingGroupShares.share)\
            .join(SavingGroupCycle, SavingGroup)\
            .filter(SavingGroupCycle.id == SavingGroupShares.sg_cycle_id)\
            .filter(SavingGroupCycle.id == cycle.id)\
            .filter(SavingGroup.id == SavingGroupShares.saving_group_id)\
            .filter(SavingGroup.id == sg_id).first()[0]

        return round(saving/shares, 1)


class SavingGroupFines(db.Model):
    __tablename__ = 'sg_fines'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    fine_type = db.Column(db.Integer)  # 1 variant  | 2 fixed
    name = db.Column(db.String(40))
    acronym = db.Column(db.String(10))
    fine = db.Column(db.Integer)
    saving_group_id = db.Column(db.Integer, db.ForeignKey('saving_group.id'), index=True)
    sg_cycle_id = db.Column(db.Integer, db.ForeignKey('sg_cycle.id'), index=True)
    db.Index('unique_fine', saving_group_id, sg_cycle_id, name, unique=True)
    member_fine = db.relationship('MemberFine', backref='sg_fines', lazy='dynamic')

    def get_url(self):
        return url_for('api.get_sg_fine', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'id': self.id,
            'date': self.date,
            'type': self.fine_type,
            'name': self.name,
            'acronyms': self.acronym,
            'fine': self.fine
        }

    def import_data(self, data):
        try:
            self.fine_type = data['type']
            self.name = data['name']
            self.fine = data['fine']
            self.acronym = self.acronyms(data['name'].split())
        except KeyError as e:
            ValidationError('Invalid SavingGroupFines ' + e.args[0])
        return self

    @staticmethod
    def fine_types(index):
        type_ = ['variant', 'fixed']
        return type_[index-1]

    @staticmethod
    def acronyms(words):
        return ''.join(w[0].upper() for w in words)


class MemberFine(db.Model):
    __tablename__ = 'member_fine'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, default=0)  # 1 Payed | 0 Not payed
    initialization_date = db.Column(db.DateTime, default=datetime.utcnow())
    payment_date = db.Column(db.DateTime, nullable=True)
    initiate_by = db.Column(db.Integer, index=True)  # admin member
    member_id = db.Column(db.Integer, db.ForeignKey('sg_member.id'), index=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('sg_wallet.id'), index=True)
    sg_fine_id = db.Column(db.Integer, db.ForeignKey('sg_fines.id'), index=True)

    def get_url(self):
        return url_for('api.get_fine', id=self.id, _external=True)

    def export_data(self):
        return {
            'id':self.id,
            'status': self.get_status(self.status),
            'initialization_date': self.initialization_date,
            'payment_date': self.payment_date,
            'self_url': self.get_url(),
            'fines': self.sg_fines.export_data(),
            'initiator_url': url_for('api.get_sg_member', id=self.initiate_by, _external=True),
            'member_url': url_for('api.get_sg_member', id=self.member_id, _external=True)
        }

    def import_data(self, data):
        try:
            self.initiate_by = data['initiate_by']
        except KeyError as e:
            ValidationError('Invalid Member Fine ' + e.args[0])
        return self

    def repay_fine(self):
        self.status = 1
        self.payment_date = datetime.utcnow()
        return self

    @staticmethod
    def get_status(status):
        value = ['not payed','payed']
        return value[status]

    @classmethod
    def fixed_fine(cls, member_id, cycle_id):
        return db.session\
            .query(func.sum(SavingGroupFines.fine).label('fines'), SavingGroupFines.name, SavingGroupFines.acronym)\
            .join(MemberFine, SavingGroupMember)\
            .filter(MemberFine.member_id == SavingGroupMember.id)\
            .filter(SavingGroupFines.id == MemberFine.sg_fine_id)\
            .filter(SavingGroupMember.id == member_id)\
            .filter(SavingGroupFines.sg_cycle_id == cycle_id)\
            .filter(SavingGroupFines.acronym != 'LRF')\
            .group_by(SavingGroupFines.name, SavingGroupFines.acronym).all()


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
    sg_fines = db.relationship('SavingGroupFines', backref='sg_cycle', lazy='dynamic')
    sg_shares = db.relationship('SavingGroupShares', backref='sg_cycle', lazy='dynamic')
    sg_meeting = db.relationship('SavingGroupMeeting', backref='sg_cycle', lazy='dynamic')
    sg_member = db.relationship('SavingGroupMember', backref='sg_cycle', lazy='dynamic')
    share_out = db.relationship('SavingGroupShareOut', backref='sg_cycle', lazy='dynamic')
    db.Index('unique_cycle', start, end, saving_group_id, unique=True)

    def get_url(self):
        return url_for('api.get_cycle', id=self.id, _external=True)

    def export_data(self):
        return {
            'id': self.id,
            'start': self.start,
            'end': self.end,
            'active': self.active,
            'cycle_length': monthdelta(self.start, self.end),
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
    activate = db.Column(db.Integer, default=1)  # 1 Activate | 0 Removed
    sg_cycle_id = db.Column(db.Integer, db.ForeignKey('sg_cycle.id'), index=True)

    member_loan = db.relationship('MemberLoan', backref='sg_member', lazy='dynamic')
    approved_loan = db.relationship('MemberApprovedLoan', backref='sg_member', lazy='dynamic')
    member_social = db.relationship('MemberSocialFund', backref='sg_member', lazy='dynamic')
    approve_social = db.relationship('MemberApprovedSocial', backref='sg_member', lazy='dynamic')
    member_fine = db.relationship('MemberFine', backref='sg_member', lazy='dynamic')
    contribution = db.relationship('SgMemberContributions', backref='sg_member', lazy='dynamic')
    member_mini_statement = db.relationship('MemberMiniStatement', backref='sg_member', lazy='dynamic')
    meeting_attendance = db.relationship('MeetingAttendance', backref='sg_member', lazy='dynamic')
    member_drop_out = db.relationship('SavingGroupDropOut', backref='sg_member', lazy='dynamic')

    db.Index('member_sg_index', saving_group_id, user_id, unique=True)

    def set_pin(self, pin):
        self.pin = generate_password_hash(pin)

    def verify_pin(self, pin):
        return check_password_hash(self.pin, pin)

    def reset_pin(self):
        self.pin = None
        return True

    def get_url(self):
        return url_for('api.get_sg_member', id=self.id, _external=True)

    def export_data(self):
        return {
            'id': self.id,
            'user_url': url_for('api.get_user', id=self.user_id, _external=True),
            'admin': self.admin,
            'date': self.date,
            'user': self.users.export_data(),
            'user_id': self.user_id,
            'self_url': self.get_url(),
            'activate': self.activate,
            'sg_url': url_for('api.get_sg', id=self.saving_group_id, _external=True),
            'approved_loan_url': url_for('api.get_member_approve_loan', id=self.id, _external=True),
            'pending_loan_url': url_for('api.get_member_pending_loan', id=self.id, _external=True),
            'approved_social_fund_url': url_for('api.get_member_approve_social_fund', id=self.id, _external=True),
            'pending_social_fund_url': url_for('api.get_member_pending_social_fund', id=self.id, _external=True),
            'member_fine': url_for('api.get_member_fine', id=self.id, _external=True),
            'member_savings_url': url_for('api.get_member_savings', id=self.id, _external=True),
            'member_social_fund_url': url_for('api.get_member_social_fund', id=self.id, _external=True),
            'member_shares': url_for('api.get_member_shares', id=self.id, _external=True)
        }

    def import_data(self, data):
        try:
            self.user_id = data['user_id']
            self.admin = data['admin']
        except KeyError as e:
            raise ValidationError('Invalid sg_member '+ e.args[0])
        return self

    def drop_out(self):
        self.activate = 0

    @classmethod
    def group_admin(cls, saving_group_id):
        return SavingGroupMember.query.\
                filter(and_(SavingGroupMember.saving_group_id == saving_group_id,
                            SavingGroupMember.admin == 1))

    @classmethod
    def count_group_admin(cls, saving_group_id):
        return db.session.query(func.count(SavingGroupMember.id)).\
            filter(and_(SavingGroupMember.saving_group_id == saving_group_id,
                        SavingGroupMember.admin == 1)).first()


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
            'format_date': arrow.get(self.date).to('Africa/Kigali').humanize(),
            'member_id': self.member_id,
            'member_url': url_for('api.get_sg_member', id=self.member_id, _external=True),
            'statement': self.statement(),
            'self_url': self.get_url(),
            'date': self.date
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
    member_id = db.Column(db.Integer, db.ForeignKey('sg_member.id'), index=True)
    sg_cycle_id = db.Column(db.Integer, db.ForeignKey('sg_cycle.id'), index=True)

    def get_url(self):
        return url_for('api.get_member_drop', id=self.id, _external=True)

    def export_data(self):
        return {
            'id': self.id,
            'date': self.date,
            'member_id': self.member_id,
            'cycle_id': self.sg_cycle_id
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
            self.name = data['name']
            self.type = data['type']
            self.account = data['account']
        except KeyError as e:
            raise ValidationError('Invalid financial: missing ' + e.args[0])
        return self


class SavingGroupMeeting(db.Model):
    __tablename__ = 'sg_meeting'
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(64))
    meeting_date = db.Column(db.Date)
    bank_balance = db.Column(db.Integer)
    external_debt = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    saving_group_id = db.Column(db.Integer, db.ForeignKey('saving_group.id'), index=True)
    cycle_id = db.Column(db.Integer, db.ForeignKey('sg_cycle.id'), index=True)

    meeting_attendance = db.relationship('MeetingAttendance', backref='sg_meeting', lazy='dynamic')

    def get_url(self):
        return url_for('api.get_meeting', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'theme': self.theme,
            'id': self.id,
            'meeting_date': self.meeting_date
        }

    def import_data(self, data):
        try:
            self.theme = data['theme']
            self.meeting_date = datetime.strptime(data['meeting_date'], "%Y-%m-%d").date()
            self.bank_balance = data['bank_balance']
            self.external_debt = data['external_debt']
        except KeyError as e:
            raise ValidationError('Invalid SG_Meeting' + e.args[0])
        return self


class MeetingAttendance(db.Model):
    __tablename__ = 'meeting_attendance'
    id = db.Column(db.Integer, primary_key=True)
    sg_meeting_id = db.Column(db.Integer, db.ForeignKey('sg_meeting.id'), index=True)
    member_id = db.Column(db.Integer, db.ForeignKey('sg_member.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    db.Index('unique_attendee', sg_meeting_id, member_id, unique=True)

    def get_url(self):
        return url_for('api.get_attendee', id=self.id, _external=True)

    def export_data(self):
        return {
            'sg_meeting_id': self.sg_meeting_id,
            'member_id': self.member_id,
            'created_at': self.created_at
        }

    def import_data(self, data):
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
    project_agent = db.relationship('ProjectAgent', backref='project', lazy='dynamic')
    saving_group = db.relationship('SavingGroup', backref='project', lazy='dynamic')
    project_partner = db.relationship('ProjectPartner', backref='project', lazy='dynamic')

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
            'saving_groups_url': url_for('api.get_project_sgs', id=self.id, _external=True),
            'intl_ngo_url': url_for('api.get_organization', id=self.id, _external=True)

        }

    def import_data(self, data):
        try:
            self.name = data['name']
            self.start = data['start']
            self.end = data['end']
            self.budget = data['budget']
            self.donor = data['donor']
            self.user_id = data['user_id']

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
            'date': self.date,
            'users': self.users.export_data()
        }

    def import_data(self, data):
        try:
            self.user_id = data['user_id']
        except KeyError as e:
            raise ValidationError('Invalid ProjectAgent: missing ' + e.args[0])
        return self


class ProjectPartner(db.Model):
    __tablename__ = 'project_partner'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), index=True)
    partner_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def get_url(self):
        return url_for('api.get_project_partner', id=self.id, _external=True)

    def export_data(self):
        return {
            'project_url': url_for('api.get_project', id=self.project_id, _external=True),
            'partner_url': url_for('api.get_organization', id=self.partner_id, _external=True),
            'date': self.date
        }


class InterventionArea(db.Model):
    __tablename__ = 'intervention_area'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    village_id = db.Column(db.Integer)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), index=True)

    def get_url(self):
        return url_for('api.get_intervention_area', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'date': self.date,
            'village': self.village_id
        }

    def export_agent_project(self):
        return {
            'project': self.project.export_data()
        }

    def import_data(self, data):
        try:
            self.village_id = int(data['village_id'])
        except KeyError as e:
            raise ValidationError('Invalid order: missing ' + e.args[0])
        return self


class Village(db.Model):
    __tablename__ = 'village'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    code = db.Column(db.String(20), unique=True)
    #intervention = db.relationship('InterventionArea', backref='village', lazy='dynamic')
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
