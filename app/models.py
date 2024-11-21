from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


def create_admin_user():
    admin = Admin.query.filter_by(name='admin').first()
    if not admin:
        new_admin = Admin(name='admin', password=generate_password_hash('password', method='sha256'))
        db.session.add(new_admin)
        db.session.commit()


class Committee(db.Model):
    __tablename__ = 'committees'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    info = db.Column(db.Text, nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('committees.id'), nullable=True)
    parent = db.relationship('Committee', remote_side=[id], backref=db.backref('sub_committees', lazy=True))

    __table_args__ = (
        UniqueConstraint('parent_id', 'name', name='uix_parent_name'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'info': self.info,
            'parent_id': self.parent_id,
            'sub_committees': [sub.to_dict() for sub in self.sub_committees]
        }


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post = db.Column(db.Text, nullable=False)
    subdivision = db.Column(db.String, nullable=False)
    created_at = db.Column(db.String, nullable=False)
    committee_id = db.Column(db.Integer, db.ForeignKey('committees.id'))
    committee = db.relationship('Committee', backref=db.backref('users', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'post': self.post,
            'subdivision': self.subdivision,
            'committee_id': self.committee_id,
            'created_at': self.created_at,
            'committee': self.committee.to_dict() if self.committee else None,
        }


class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'), nullable=False)
    response_time = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    survey = db.relationship('Survey', backref=db.backref('records', lazy=True))
    user = db.relationship('User', backref=db.backref('records', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'survey_id': self.survey_id,
            'response_time': self.response_time,
            'created_at': self.created_at,
            'user': self.user.to_dict() if self.user else None
        }


class SurveySettings(db.Model):
    __tablename__ = "survey_settings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    key = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False, unique=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id', ondelete='CASCADE'))

    def to_dict(self):
        return {
            'id': self.id,
            "name": self.name,
            'key': self.key,
            'value': self.value,
            'survey_id': self.survey_id
        }


class Survey(db.Model):
    __tablename__ = 'surveys'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, unique=True, nullable=False)
    introduction = db.Column(db.String, nullable=True)
    directions = db.relationship('Direction', backref='survey', lazy=True)
    survey_instructions = db.relationship('SurveyInstruction', backref='survey', lazy=True)
    survey_settings = db.relationship("SurveySettings", backref='survey', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'introduction': self.introduction,
            'directions': [direction.to_dict() for direction in self.directions],
            'survey_instructions': [instruction.to_dict() for instruction in self.survey_instructions],
            'survey_settings': [settings.to_dict() for settings in self.survey_settings]
        }


class SurveyInstruction(db.Model):
    __tablename__ = 'survey_instructions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    body_html = db.Column(db.String, nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id', ondelete='CASCADE'))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body_html': self.body_html,
            'survey_id': self.survey_id
        }


class ContactInfo(db.Model):
    __tablename__ = 'contact_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'phone': self.phone
        }


class Settings(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String, unique=True, nullable=False)
    value = db.Column(db.String, unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value
        }


class Direction(db.Model):
    __tablename__ = 'directions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    coefficient = db.Column(db.Integer, nullable=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id', ondelete='CASCADE'))
    criterions = db.relationship('Criterion', backref='direction', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'coefficient': self.coefficient,
            'survey_id': self.survey_id,
            'criterions': [criterion.to_dict() for criterion in self.criterions]
        }


class Criterion(db.Model):
    __tablename__ = 'criterions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    number = db.Column(db.String, nullable=False)
    question_number = db.Column(db.Integer, default=0, nullable=False)
    weight = db.Column(db.Float, nullable=True)
    question = db.Column(db.String, default=None, nullable=True)
    prompt = db.Column(db.String, default=None, nullable=True)
    is_interview = db.Column(db.Boolean, default=False, nullable=True)
    detailed_response = db.Column(db.Boolean, default=False, nullable=True)
    direction_id = db.Column(db.Integer, db.ForeignKey('directions.id'), nullable=False)
    subcriterions = db.relationship('Subcriterion', backref='criterion', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'number': self.number,
            'question_number': self.question_number,
            'weight': self.weight,
            'question': self.question,
            'prompt': self.prompt,
            'is_interview': self.is_interview,
            'detailed_response': self.detailed_response,
            'direction_id': self.direction_id,
            'subcriterions': [subcriterion.to_dict() for subcriterion in self.subcriterions]
        }


class Subcriterion(db.Model):
    __tablename__ = 'subcriterions'
    id = db.Column(db.Integer, primary_key=True)
    question_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    prompt = db.Column(db.String, nullable=True)
    detailed_response = db.Column(db.Boolean, default=False, nullable=True)
    criterion_id = db.Column(db.Integer, db.ForeignKey('criterions.id'), nullable=False)
    puncts = db.relationship('Punct', backref='subcriterion', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'question_number': self.question_number,
            'title': self.title,
            'weight': self.weight,
            'prompt': self.prompt,
            'detailed_response': self.detailed_response,
            'criterion_id': self.criterion_id,
            'puncts': [punct.to_dict() for punct in self.puncts]
        }


class Punct(db.Model):
    __tablename__ = 'puncts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    range_min = db.Column(db.Integer, nullable=False)
    range_max = db.Column(db.Integer, nullable=False)
    prompt = db.Column(db.String, nullable=True)
    comment = db.Column(db.String, nullable=True)
    subcriterion_id = db.Column(db.Integer, db.ForeignKey('subcriterions.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'range_min': self.range_min,
            'range_max': self.range_max,
            'prompt': self.prompt,
            'comment': self.comment,
            'subcriterion_id': self.subcriterion_id
        }


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey('records.id', ondelete='CASCADE'))
    criterion_id = db.Column(db.Integer, db.ForeignKey('criterions.id'), nullable=True)  # Answer can relate to a Criterion
    subcriterion_id = db.Column(db.Integer, db.ForeignKey('subcriterions.id'), nullable=True)  # or a Subcriterion
    punct_id = db.Column(db.Integer, db.ForeignKey('puncts.id'), nullable=True)  # or a Punct, if answer is a choice
    answer_value = db.Column(db.Float, nullable=True)  # For graded answers
    comment = db.Column(db.String, nullable=True)  # Optional comment for any answer
    range_value = db.Column(db.Float, nullable=True)

    # Relationships
    record = db.relationship('Record', backref=db.backref('answers', lazy=True))
    criterion = db.relationship('Criterion', backref=db.backref('answers', lazy=True))
    subcriterion = db.relationship('Subcriterion', backref=db.backref('answers', lazy=True))
    punct = db.relationship('Punct', backref=db.backref('answers', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'record_id': self.record_id,
            'criterion_id': self.criterion_id,
            'subcriterion_id': self.subcriterion_id,
            'punct_id': self.punct_id,
            'answer_value': self.answer_value,
            'comment': self.comment,
            'range_value': self.range_value,
            'record': self.record.to_dict() if self.record else None
        }


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Feedback {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'message': self.message,
            'submitted_at': self.submitted_at
        }
