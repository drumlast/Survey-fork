from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, RadioField, FieldList, \
    FormField, BooleanField, DecimalField, FloatField
from wtforms.validators import DataRequired, EqualTo, Email, Optional


class AdminLoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')


class SurveyCreateForm(FlaskForm):
    submit = SubmitField('Закончить опрос')


class FeedbackForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    email = StringField('Ваш Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class CommitteeForm(FlaskForm):
    name = StringField('Название комитета', validators=[DataRequired()])
    info = TextAreaField('Информация о комитете')
    parent_id = SelectField('Родительский комитет', coerce=int, choices=[])
    submit = SubmitField('Добавить комитет')


class CommitteeRegistrationForm(FlaskForm):
    committee = SelectField('Выберите ваш ИОГВ', validators=[DataRequired()], choices=[])
    subdivision = StringField('Ваше подразделение', validators=[DataRequired()])
    post = StringField('Введите вашу должность', validators=[DataRequired()])
    privacy = BooleanField('Я принимаю политику конфиденциальности', validators=[DataRequired()])
    submit = SubmitField('Регистрация')


class SurveySlugForm(FlaskForm):
    title = StringField('Название опроса', validators=[DataRequired()])
    slug = StringField('Идентификатор URL (slug)', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class PunctForm(FlaskForm):
    title = StringField('Точка ответа', render_kw={"readonly": True})
    range_min = FloatField('Минимум', render_kw={"readonly": True})
    range_max = FloatField('Максимум', render_kw={"readonly": True})
    selected_score = FloatField('Выбранная оценка', validators=[DataRequired()])


class SubcriterionForm(FlaskForm):
    title = StringField('Заголовок', render_kw={"readonly": True})
    weight = FloatField('Вес', render_kw={"readonly": True})
    comment = TextAreaField('Комментарий', validators=[Optional()])
    puncts = FieldList(FormField(PunctForm), min_entries=1)


class CriterionForm(FlaskForm):
    title = StringField('Заголовок', render_kw={"readonly": True})
    weight = FloatField('Вес', render_kw={"readonly": True})
    subcriteria = FieldList(FormField(SubcriterionForm), min_entries=1)


class DirectionForm(FlaskForm):
    title = StringField('Направление', render_kw={"readonly": True})
    criterions = FieldList(FormField(CriterionForm), min_entries=1)


class SurveyForm(FlaskForm):
    directions = FieldList(FormField(DirectionForm), min_entries=1)
    submit = SubmitField('Закончить опрос')
