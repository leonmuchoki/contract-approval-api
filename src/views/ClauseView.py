from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.ClauseModel import ClauseModel, ClauseSchema
from ..models.ClausePartModel import ClausePartModel

clause_api = Blueprint('clause_api', __name__)
clause_schema = ClauseSchema()


@clause_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
	"""
	Create Clause Function
	"""
	req_data = request.get_json()
	req_data['created_by'] = g.user.get('id')

	contract_clause = ClauseModel(req_data)
	contract_clause.save()
	data = clause_schema.dump(req_data)
	return custom_response(data, 201)


@clause_api.route('/', methods=['GET'])
def get_all():
	"""
	Get All Clauses
	"""
	clauses = ClauseModel.get_all_clauses()
	data = clause_schema.dump(clauses, many=True)
	return custom_response(data, 200)

@clause_api.route('/parts', methods=['GET'])
def get_clause_parts():
	"""
	Get All Clause Parts
	"""
	clause_parts = ClausePartModel.get_all_clause_parts()
	data = clause_schema.dump(clause_parts, many=True)
	return custom_response(data, 200)


@clause_api.route('/<int:clause_id>', methods=['GET'])
def get_one(clause_id):
	"""
	Get A Clause
	"""
	clause = ClauseModel.get_one_clause(clause_id)
	if not clause:
		return custom_response({'error': 'clause not found'}, 404)
	data = clause_schema.dump(clause)
	return custom_response(data, 200)


@clause_api.route('/<int:clause_id>', methods=['PUT'])
@Auth.auth_required
def update(clause_id):
	"""
	Update A Clause
	"""
	req_data = request.get_json()
	clause = ClauseModel.get_one_clause(clause_id)
	if not clause:
		return custom_response({'error': ' clause not found'}, 404)
	clause = clause_schema.dump(clause)
	if clause.get('created_by') != g.user.get('id'):
		return custom_response({'error': 'permission denied'}, 400)

	data, error = clause_schema.load(req_data, partial=True)
	if error:
		return custom_response(error, 400)
	clause.update(data)

	data = clause_schema.dump(clause)
	return custom_response(data, 200)


@clause_api.route('/<int:clause_id>', methods=['DELETE'])
@Auth.auth_required
def delete(clause_id):
	"""
	Delete A Clause
	"""
	clause = ClauseModel.get_one_clause(clause_id)
	if not clause:
		return custom_response({'error': ' clause not found'}, 404)
	data = clause_schema.dump(clause)
	if data.get('created_by') != g.user.get('id'):
		return custom_response({'error': 'permission denied'}, 400)

	clause.delete()
	return custom_response({'message': 'deleted'}, 204)


def custom_response(res, status_code):
	"""
	Custom Response Function
	"""
	return Response(
		mimetype="application/json",
		response=json.dumps(res),
		status=status_code
	)
