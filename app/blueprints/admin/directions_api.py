from flask import Blueprint, request, flash, redirect, url_for, render_template, jsonify
from flask_login import login_required

from app.models import Direction, db

direction_api = Blueprint('direction_api', __name__, template_folder='templates/admin')


@direction_api.route('/add_direction', methods=['GET', 'POST'])
def add_direction():
    if request.method == 'POST':
        title = request.form['title']
        new_direction = Direction(title=title)
        db.session.add(new_direction)
        db.session.commit()
        flash('Новое направление добавлено!')
        return redirect(url_for('admin.questions'))
    return render_template('admin/add_direction.html')


@direction_api.route('/direction/<int:direction_id>/', methods=['PUT'])
@login_required
def update_direction(direction_id):
    direction = Direction.query.get_or_404(direction_id)
    data = request.get_json()
    direction.title = data.get('title', direction.title)
    db.session.commit()
    return jsonify({'success': True})


@direction_api.route('/direction/<int:direction_id>/', methods=['DELETE'])
@login_required
def delete_direction(direction_id):
    direction = Direction.query.get_or_404(direction_id)
    db.session.delete(direction)
    db.session.commit()
    return jsonify({'success': True})
