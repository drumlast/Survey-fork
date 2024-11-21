from flask import Blueprint, jsonify

from app.forms import CommitteeForm
from app.models import Committee, db

committees_api = Blueprint('committees_api', __name__, template_folder='templates/admin')


@committees_api.route('/committees', methods=['GET'])
def api_committees():
    committees = Committee.query.all()
    return jsonify([{
        'id': committee.id,
        'name': committee.name,
        'info': committee.info,
        'parent_id': committee.parent_id
    } for committee in committees])


@committees_api.route('/committees/<int:parent_id>', methods=['GET'])
def api_sub_committees(parent_id):
    committees = Committee.query.filter_by(parent_id=parent_id).all()
    return jsonify([{
        'id': committee.id,
        'name': committee.name,
        'info': committee.info,
        'parent_id': committee.parent_id
    } for committee in committees])


@committees_api.route('/committees', methods=['POST'])
def add_committee():
    form = CommitteeForm()
    if form.validate_on_submit():
        committee = Committee(
            name=form.name.data,
            info=form.info.data,
            parent_id=form.parent_id.data if form.parent_id.data else None
        )
        db.session.add(committee)
        db.session.commit()
        return jsonify({'message': 'Комитет добавлен!'})
    return jsonify({'error': 'Ошибка при добавлении комитета.'}), 400


@committees_api.route('/committees/<int:committee_id>', methods=['PUT'])
def edit_committee(committee_id):
    form = CommitteeForm()
    if form.validate_on_submit():
        committee = Committee.query.get_or_404(committee_id)
        committee.name = form.name.data
        committee.info = form.info.data
        committee.parent_id = form.parent_id.data if form.parent_id.data else None
        db.session.commit()
        return jsonify({'message': 'Комитет обновлен!'})
    return jsonify({'error': 'Invalid data'}), 400


@committees_api.route('/committees/<int:committee_id>', methods=['DELETE'])
def delete_committee(committee_id):
    committee = Committee.query.get_or_404(committee_id)
    db.session.delete(committee)
    db.session.commit()
    return jsonify({'message': 'Комитет удален!'})
