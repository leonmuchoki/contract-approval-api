from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.ContractClauseDetailsModel import ContractClauseDetailModel, ContractClauseDetailsSchema

contract_clause_details_api = Blueprint('contract_clause_details_api', __name__)
contract_clause_detail_schema = ContractClauseDetailsSchema()

@contract_clause_details_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
	"""
	Create Contract Clause Details Function
	"""
	req_data = request.get_json()
	req_data['created_by'] = g.user.get('id')

	cd = ContractClauseDetailModel(req_data)
	cd.save()
	data = contract_clause_detail_schema.dump(cd)
	return custom_response(data, 201)


@contract_clause_details_api.route('/', methods=['GET'])
def get_all():
	"""
	Get All Contract  Clause Details
	"""
	contract_clause_details = ContractClauseDetailModel.get_all_contract_clauses()
	data = contract_clause_detail_schema.dump(contract_clause_details, many=True)
	return custom_response(data, 200)


@contract_clause_details_api.route('/<int:contract_clause_details_id>', methods=['GET'])
def get_one(contract_clause_details_id):
	"""
	Get A Contract Clause Details
	"""
	contract_clause_detail = ContractClauseDetailModel.get_one_contract_clause(contract_clause_details_id)
	if not post:
		return custom_response({'error': 'contract_clause_detail not found'}, 404)
	data = contract_clause_detail_schema.dump(contract_clause_detail)
	return custom_response(data, 200)


@contract_clause_details_api.route('/<int:contract_clause_details_id>', methods=['PUT'])
@Auth.auth_required
def update(contract_clause_details_id):
	"""
	Update A Contract Clause Details
	"""
	req_data = request.get_json()
	contract_clause_detail = ContractClauseDetailModel.get_one_contract_clause(contract_clause_details_id)
	if not contract_clause_detail:
		return custom_response({'error': 'contract clause detail not found'}, 404)
	data = contract_clause_detail_schema.dump(contract_clause_detail)
	if data.get('created_by') != g.user.get('id'):
		return custom_response({'error': 'permission denied'}, 400)

	data, error = contract_clause_detail_schema.load(req_data, partial=True)
	if error:
		return custom_response(error, 400)
	contract_clause_detail.update(data)

	data = contract_clause_detail_schema.dump(contract_clause_detail)
	return custom_response(data, 200)


@contract_clause_details_api.route('/<int:contract_clause_details_id>', methods=['DELETE'])
@Auth.auth_required
def delete(contract_clause_details_id):
	"""
	Delete A Contract Clause Detail
	"""
	contract_clause_detail = ContractClauseDetailModel.get_one_contract_clause(contract_clause_details_id)
	if not contract_clause_detail:
		return custom_response({'error': 'contract clause detail not found'}, 404)
	data = contract_clause_detail_schema.dump(contract_clause_detail)
	if data.get('created_by') != g.user.get('id'):
		return custom_response({'error': 'permission denied'}, 400)

	contract_clause_detail.delete()
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
