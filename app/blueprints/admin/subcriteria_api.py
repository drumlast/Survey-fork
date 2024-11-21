from flask import Blueprint, request, flash, redirect, url_for, render_template, jsonify
from flask_login import login_required

from app.models import Criterion, Subcriterion, db

subcriteria_api = Blueprint('subcriteria_api', __name__, template_folder='templates/admin')


@subcriteria_api.route('/add_subcriterion', methods=['GET', 'POST'])
def add_subcriterion():
    criterions = Criterion.query.all()
    if request.method == 'POST':
        title = request.form['title']
        criterion_id = request.form['criterion_id']
        new_subcriterion = Subcriterion(title=title, criterion_id=criterion_id)
        db.session.add(new_subcriterion)
        db.session.commit()
        flash('Новый подкритерий добавлен!')
        return redirect(url_for('admin.questions'))
    return render_template('admin/add_subcriterion.html', criterions=criterions)


@subcriteria_api.route('/subcriterion/<int:subcriterion_id>/', methods=['PUT'])
@login_required
def update_subcriterion(subcriterion_id):
    subcriterion = Subcriterion.query.get_or_404(subcriterion_id)
    data = request.get_json()
    subcriterion.title = data.get('title', subcriterion.title)
    subcriterion.weight = data.get('weight', subcriterion.weight)
    subcriterion.prompt = data.get('prompt', subcriterion.prompt)
    subcriterion.detailed_response = data.get('detailed_response', subcriterion.detailed_response)
    db.session.commit()
    return jsonify({'success': True})


@subcriteria_api.route('/subcriterion/<int:subcriterion_id>/', methods=['DELETE'])
@login_required
def delete_subcriterion(subcriterion_id):
    subcriterion = Subcriterion.query.get_or_404(subcriterion_id)
    db.session.delete(subcriterion)
    db.session.commit()
    return jsonify({'success': True})
