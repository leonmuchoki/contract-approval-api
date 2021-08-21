from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.ContractClauseModel import ContractClauseModel, ContractClauseSchema

contract_clause_api = Blueprint('contract_clause_api', __name__)
contract_clause_schema = ContractClauseSchema()


@contract_clause_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
	"""
	Create Contract Clause Function
	"""
	req_data = request.get_json()
	req_data['created_by'] = g.user.get('id')

	contract_clause = ContractClauseModel(req_data)
	contract_clause.save()
	data = contract_clause_schema.dump(req_data)
	return custom_response(data, 201)


@contract_clause_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
	"""
	Get All Contract Clauses
	"""
	contract_clauses = ContractClauseModel.get_all_contract_clauses()
	data = contract_clause_schema.dump(contract_clauses, many=True)
	return custom_response(data, 200)


@contract_clause_api.route('/<int:contract_clause_id>', methods=['GET'])
@Auth.auth_required
def get_one(contract_clause_id):
	"""
	Get A Contract Clause
	"""
	contract_clause = ContractClauseModel.get_one_contract_clause(contract_clause_id)
	if not contract_clause:
		return custom_response({'error': 'contract clause not found'}, 404)
	data = contract_clause_schema.dump(contract_clause)
	return custom_response(data, 200)


@contract_clause_api.route('/<int:contract_clause_id>', methods=['PUT'])
@Auth.auth_required
def update(contract_clause_id):
	"""
	Update A Contract Clause
	"""
	req_data = request.get_json()
	post = ContractClauseModel.get_one_contract_clause(contract_clause_id)
	if not post:
		return custom_response({'error': 'contract clause not found'}, 404)
	data = contract_clause_schema.dump(post).data
	if data.get('created_by') != g.user.get('id'):
		return custom_response({'error': 'permission denied'}, 400)

	data, error = contract_clause_schema.load(req_data, partial=True)
	if error:
		return custom_response(error, 400)
	post.update(data)

	data = contract_clause_schema.dump(post).data
	return custom_response(data, 200)


@contract_clause_api.route('/<int:contract_clause_id>', methods=['DELETE'])
@Auth.auth_required
def delete(contract_clause_id):
	"""
	Delete A Contract Clause
	"""
	post = ContractClauseModel.get_one_contract_clause(contract_clause_id)
	if not post:
		return custom_response({'error': 'contract clause not found'}, 404)
	data = contract_clause_schema.dump(post).data
	if data.get('created_by') != g.user.get('id'):
		return custom_response({'error': 'permission denied'}, 400)

	post.delete()
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
