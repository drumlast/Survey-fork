from flask import Blueprint, request, flash, redirect, url_for, render_template, jsonify
from flask_login import login_required

from app.models import Subcriterion, Punct, db

puncts_api = Blueprint('puncts_api', __name__, template_folder='templates/admin')


@puncts_api.route('/add_punct', methods=['GET', 'POST'])
def add_punct():
    subcriterions = Subcriterion.query.all()
    if request.method == 'POST':
        title = request.form['title']
        range_min = request.form['range_min']
        range_max = request.form['range_max']
        subcriterion_id = request.form['subcriterion_id']
        new_punct = Punct(title=title, range_min=range_min, range_max=range_max, subcriterion_id=subcriterion_id)
        db.session.add(new_punct)
        db.session.commit()
        flash('Новый вопрос добавлен!')
        return redirect(url_for('admin.questions'))
    return render_template('admin/add_punct.html', subcriterions=subcriterions)


# Обновление пунктаx
@puncts_api.route('/punct/<int:punct_id>/', methods=['PUT'])
@login_required
def update_punct(punct_id):
    punct = Punct.query.get_or_404(punct_id)
    data = request.get_json()
    punct.title = data.get('title', punct.title)
    punct.range_min = data.get('range_min', punct.range_min)
    punct.range_max = data.get('range_max', punct.range_max)
    punct.prompt = data.get('prompt', punct.prompt)
    punct.comment = data.get('comment', punct.comment)
    db.session.commit()
    return jsonify({'success': True})


@puncts_api.route('/punct/<int:punct_id>/', methods=['DELETE'])
@login_required
def delete_punct(punct_id):
    punct = Punct.query.get_or_404(punct_id)
    db.session.delete(punct)
    db.session.commit()
    return jsonify({'success': True})
