import random
from datetime import datetime, timedelta
from pathlib import Path

from app.models import User, Record, Answer, Committee, Criterion, Subcriterion, db


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def generate_random_reports():
    committees = Committee.query.all()
    criteria = Criterion.query.all()

    records_to_add = []
    answers_to_add = []

    for committee in committees:
        num_reports = random.randint(5, 100)  # Генерация от 5 до 100 отчётов на комитет

        for _ in range(num_reports):
            # Создание пользователя
            post = f"Должность №{random.randint(1, 100)}"
            subdivision = f"Подразделение №{random.randint(1, 50)}"
            created_at = datetime.utcnow() - timedelta(days=random.randint(1, 30))

            user = User(
                post=post,
                subdivision=subdivision,
                committee_id=committee.id,
                created_at=created_at
            )
            db.session.add(user)
            db.session.flush()

            # Создание записи отчёта
            record = Record(
                user_id=user.id,
                survey_id=1,  # ID нужного опроса
                created_at=created_at
            )
            records_to_add.append(record)
            db.session.add(record)
            db.session.flush()

            # Обработка критериев и их подкритериев
            for criterion in criteria:
                subcriteria = Subcriterion.query.filter_by(criterion_id=criterion.id).all()

                if subcriteria:
                    # Если у критерия есть подкритерии, генерируем данные только для подкритериев
                    for subcriterion in subcriteria:
                        if subcriterion.detailed_response:
                            # Интервью для подкритерия с градацией от 0 до 4
                            range_value = random.choice([i * 0.25 for i in range(17)])  # от 0 до 4 с шагом 0.25
                            comment = f"Тестовый ответ для интервью подкритерия {subcriterion.id}"
                            answer = Answer(
                                record_id=record.id,
                                criterion_id=criterion.id,
                                subcriterion_id=subcriterion.id,
                                answer_value=None,
                                range_value=range_value,
                                comment=comment
                            )
                        else:
                            # Обычный ответ для подкритерия
                            answer_value = random.choice([0, 1, 2, 3])
                            range_value = random.choice([0.0, 0.25, 0.5, 0.75, 1.0])
                            comment = f"Тестовый комментарий для подкритерия {subcriterion.id}"
                            answer = Answer(
                                record_id=record.id,
                                criterion_id=criterion.id,
                                subcriterion_id=subcriterion.id,
                                answer_value=answer_value,
                                range_value=range_value,
                                comment=comment
                            )
                        answers_to_add.append(answer)
                else:
                    # Если у критерия нет подкритериев, генерируем данные для самого критерия
                    if criterion.detailed_response:
                        # Интервью для критерия с градацией от 0 до 4
                        range_value = random.choice([i * 0.25 for i in range(17)])
                        comment = f"Тестовый ответ для интервью критерия {criterion.id}"
                        answer = Answer(
                            record_id=record.id,
                            criterion_id=criterion.id,
                            subcriterion_id=None,
                            answer_value=None,
                            range_value=range_value,
                            comment=comment
                        )
                    else:
                        # Обычный ответ для критерия
                        answer_value = random.choice([0, 1, 2, 3])
                        range_value = random.choice([0.0, 0.25, 0.5, 0.75, 1.0])
                        comment = f"Тестовый комментарий для критерия {criterion.id}"
                        answer = Answer(
                            record_id=record.id,
                            criterion_id=criterion.id,
                            subcriterion_id=None,
                            answer_value=answer_value,
                            range_value=range_value,
                            comment=comment
                        )
                    answers_to_add.append(answer)

    # Сохранение данных в базе
    db.session.bulk_save_objects(records_to_add)
    db.session.bulk_save_objects(answers_to_add)
    db.session.commit()
