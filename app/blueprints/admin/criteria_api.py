from flask import request, flash, redirect, url_for, render_template, Blueprint, jsonify
from flask_login import login_required

from app.models import Direction, Criterion, db

criteria_api = Blueprint('criteria_api', __name__, template_folder='templates/admin')


@criteria_api.route('/add_criterion', methods=['GET', 'POST'])
def add_criterion():
    directions = Direction.query.all()
    if request.method == 'POST':
        title = request.form['title']
        number = request.form['number']
        direction_id = request.form['direction_id']
        new_criterion = Criterion(title=title, number=number, direction_id=direction_id)
        db.session.add(new_criterion)
        db.session.commit()
        flash('Новый критерий добавлен!')
        return redirect(url_for('admin.questions'))
    return render_template('admin/add_criterion.html', directions=directions)


@criteria_api.route('/edit_criterion/<int:criterion_id>', methods=['GET', 'POST'])
def edit_criterion(criterion_id):
    criterion = Criterion.query.get_or_404(criterion_id)
    directions = Direction.query.all()
    if request.method == 'POST':
        criterion.title = request.form['title']
        criterion.number = request.form['number']
        criterion.direction_id = request.form['direction_id']
        db.session.commit()
        flash('Критерий обновлен!')
        return redirect(url_for('admin.questions'))
    return render_template('admin/edit_criterion.html', criterion=criterion, directions=directions)


@criteria_api.route('/criterion/<int:criterion_id>/', methods=['PUT'])
@login_required
def update_criterion(criterion_id):
    criterion = Criterion.query.get_or_404(criterion_id)
    data = request.get_json()
    criterion.title = data.get('title', criterion.title)
    criterion.number = data.get('number', criterion.number)
    criterion.weight = data.get('weight', criterion.weight)
    criterion.prompt = data.get('prompt', criterion.prompt)
    criterion.question = data.get('question', criterion.question)
    criterion.detailed_response = data.get('detailed_response', criterion.detailed_response)
    criterion.is_interview = data.get('is_interview', criterion.is_interview)
    db.session.commit()
    return jsonify({'success': True})


@criteria_api.route('/criterion/<int:criterion_id>/', methods=['DELETE'])
@login_required
def delete_criterion(criterion_id):
    criterion = Criterion.query.get_or_404(criterion_id)
    db.session.delete(criterion)
    db.session.commit()
    return jsonify({'success': True})
