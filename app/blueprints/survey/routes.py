import json
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_wtf.csrf import validate_csrf

from app import db
from app.forms import FeedbackForm, SurveyForm
from app.models import ContactInfo, Survey, Committee, Answer, Record, User, Punct, Subcriterion, Criterion, Feedback
from app.schemas import SurveySchema, CommitteeSchema

survey_bp = Blueprint('survey', __name__, template_folder='templates/survey')


@survey_bp.route('/')
def index():
    surveys = Survey.query.all()
    return render_template('survey/index.html', surveys=surveys)


@survey_bp.route('/survey/<slug>', methods=['GET', 'POST'])
def take_survey(slug):
    survey_data = Survey.query.filter_by(slug=slug).first_or_404()
    survey = SurveySchema.model_validate(survey_data.to_dict())
    committees = [CommitteeSchema.model_validate(committee.to_dict()) for committee in Committee.query.all()]

    if request.method == 'POST':
        form_data = request.form.to_dict()
        print(form_data)
        with open(f"reports/json/{form_data['post']}-{form_data['subdivision']}-{form_data['committee']}", "w",
                  encoding="utf-8") as file:
            json.dump(form_data, file)
        csrf_token = form_data.get('csrf_token')
        try:
            validate_csrf(csrf_token)
        except Exception as e:
            flash("Ошибка: отсутствует или неверный CSRF токен.", 'error')
            return redirect(url_for('survey_bp.take_survey', slug=slug))

        try:
            new_user = User(
                post=form_data["post"],
                subdivision=form_data["subdivision"],
                committee_id=form_data["committee"],
                created_at=datetime.utcnow()
            )
            db.session.add(new_user)
            db.session.flush()

            user_record = Record(user_id=new_user.id, survey_id=survey_data.id, created_at=datetime.utcnow())
            db.session.add(user_record)
            db.session.flush()

            answers = {}

            allowed_values = [i * 0.25 for i in range(0, 17)]

            for key, value in form_data.items():
                if key.startswith("criterion_") and key.endswith("_response"):
                    try:
                        question_number = int(key.split("_")[1])
                        answers[question_number] = {"comment": value}
                    except (IndexError, ValueError):
                        print(f"Ошибка при обработке ключа {key}: некорректный формат.")
                        continue

                elif key.endswith("-range"):
                    if key.startswith("criterion_"):
                        try:
                            question_number = int(key.split("_")[1].split("-")[0])
                            range_value = float(value)

                            if range_value in allowed_values:
                                if question_number not in answers:
                                    answers[question_number] = {}
                                answers[question_number]["range_value"] = range_value
                            else:
                                print(
                                    f"Ошибка при обработке значения {value} для {key}: значение должно быть одним из {allowed_values}.")
                        except (IndexError, ValueError) as e:
                            print(f"Ошибка при обработке значения {value} для {key}: некорректный формат. E: {e}")

                    else:
                        try:
                            question_number = int(key.split("-")[0])
                            range_value = float(value)

                            if range_value in allowed_values:
                                if question_number not in answers:
                                    answers[question_number] = {}
                                answers[question_number]["range_value"] = range_value
                            else:
                                print(
                                    f"Ошибка при обработке значения {value} для {key}: значение должно быть одним из {allowed_values}.")
                        except (IndexError, ValueError) as e:
                            print(f"Ошибка при обработке значения {value} для {key}: некорректный формат. E: {e}")

                elif "-radio" in key:
                    split_key = key.split("-")
                    if len(split_key) > 1:
                        try:
                            question_number = int(split_key[0])
                            range_min_value = float(value)
                            subcriterion = db.session.query(Subcriterion).filter_by(
                                question_number=question_number).first()

                            if subcriterion:
                                punct = db.session.query(Punct).filter_by(subcriterion_id=subcriterion.id,
                                                                          range_min=range_min_value).first()
                                if punct:
                                    punct_id = punct.id
                                    if question_number not in answers:
                                        answers[question_number] = {}
                                    answers[question_number].update({
                                        "punct_id": punct_id,
                                        "answer_value": range_min_value
                                    })
                        except ValueError:
                            print(f"Ошибка при обработке значения {value} для {key}: некорректный формат.")
                            continue

                elif key.endswith("-textarea") or key.endswith("-comment"):
                    split_key = key.split("-")
                    if len(split_key) > 1:
                        try:
                            question_number = int(split_key[0])
                            if question_number not in answers:
                                answers[question_number] = {}
                            answers[question_number]["comment"] = value
                        except ValueError:
                            print(f"Ошибка при обработке значения {value} для {key}: некорректный формат.")
                            continue

            for question_number, answer_data in answers.items():
                criterion_id = next(
                    (criterion.id for direction in survey_data.directions
                     for criterion in direction.criterions
                     if criterion.question_number == question_number),
                    None
                )

                subcriterion_id = next(
                    (sc.id for direction in survey_data.directions
                     for criterion in direction.criterions
                     for sc in criterion.subcriterions
                     if sc.question_number == question_number),
                    None
                )

                if subcriterion_id and not criterion_id:
                    criterion_id = next(
                        (criterion.id for direction in survey_data.directions
                         for criterion in direction.criterions
                         for sc in criterion.subcriterions
                         if sc.id == subcriterion_id),
                        None
                    )

                is_detailed_response_required = (
                        (criterion_id and db.session.query(Criterion)
                         .filter_by(id=criterion_id, detailed_response=True)
                         .first()) or
                        (subcriterion_id and db.session.query(Subcriterion)
                         .filter_by(id=subcriterion_id, detailed_response=True)
                         .first())
                )

                if is_detailed_response_required and "comment" not in answer_data:
                    flash(f"Вопрос {question_number} требует развернутого ответа.", 'error')
                    return redirect(url_for('survey_bp.take_survey', slug=slug))

                answer = Answer(
                    record_id=user_record.id,
                    criterion_id=criterion_id,
                    subcriterion_id=subcriterion_id,
                    punct_id=answer_data.get("punct_id"),
                    answer_value=answer_data.get("answer_value"),
                    range_value=answer_data.get("range_value"),
                    comment=answer_data.get("comment")
                )
                print(answer.to_dict())
                db.session.add(
                    answer
                )

            db.session.commit()
            flash("Ваши ответы успешно сохранены", 'success')
            return redirect(url_for('survey.index'))

        except Exception as e:
            db.session.rollback()
            flash(f"Произошла ошибка при сохранении ответов: {str(e)}", 'error')

    return render_template('survey/one_page.html', survey=survey, committees=committees, form=SurveyForm())


@survey_bp.route('/about')
def about():
    return render_template('survey/about.html', title='О сайте')


@survey_bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    contact_info = ContactInfo.query.first()
    if form.validate_on_submit():
        new_feedback = Feedback(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(new_feedback)
        db.session.commit()
        flash('Ваше сообщение было отправлено.', 'success')
        return redirect(url_for('survey.feedback'))
    return render_template('survey/feedback.html', form=form, title='Обратная связь', contact_info=contact_info)


@survey_bp.route('/privacy')
def privacy():
    return render_template('survey/privacy.html', title='Политика конфиденциальности')
