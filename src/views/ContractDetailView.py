from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.ContractDetailModel import ContractDetailModel, ContractDetailSchema

contract_detail_api = Blueprint('contract_detail_api', __name__)
contract_detail_schema = ContractDetailSchema()


@contract_detail_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
	"""
	Create Contract Detail Function
	"""
	req_data = request.get_json()
	req_data['created_by'] = g.user.get('id')
	data, error = contract_detail_schema.load(req_data)
	if error:
		return custom_response(error, 400)
	contract_detail = ContractDetailModel(data)
	contract_detail.save()
	data = contract_detail_schema.dump(contract_detail).data
	return custom_response(data, 201)


@contract_detail_api.route('/', methods=['GET'])
def get_all():
	"""
	Get All Contract Clauses
	"""
	contract_details = ContractDetailModel.get_all_contract_details()
	data = contract_detail_schema.dump(contract_details, many=True).data
	return custom_response(data, 200)


@contract_detail_api.route('/<int:contract_detail_id>', methods=['GET'])
def get_one(contract_detail_id):
	"""
	Get A Contract Detail
	"""
	contract_detail = ContractDetailModel.get_one_contract_clause(contract_detail_id)
	if not contract_detail:
		return custom_response({'error': 'contract detail not found'}, 404)
	data = contract_detail_schema.dump(contract_detail).data
	return custom_response(data, 200)


@contract_detail_api.route('/<int:contract_detail_id>', methods=['PUT'])
@Auth.auth_required
def update(contract_detail_id):
	"""
	Update A Contract Detail
	"""
	req_data = request.get_json()
	contract_detail = ContractDetailModel.get_one_contract_detail(contract_detail_id)
	if not contract_detail:
		return custom_response({'error': 'contract clause not found'}, 404)
	data = contract_detail_schema.dump(contract_detail).data
	if data.get('created_by') != g.user.get('id'):
		return custom_response({'error': 'permission denied'}, 400)

	data, error = contract_detail_schema.load(req_data, partial=True)
	if error:
		return custom_response(error, 400)
	contract_detail.update(data)

	data = contract_detail_schema.dump(contract_detail).data
	return custom_response(data, 200)


@contract_detail_api.route('/<int:contract_detail_id>', methods=['DELETE'])
@Auth.auth_required
def delete(contract_detail_id):
	"""
	Delete A Contract Detail
	"""
	contract_detail = ContractDetailModel.get_one_contract_detail(contract_detail_id)
	if not contract_detail:
		return custom_response({'error': 'contract detail not found'}, 404)
	data = contract_detail_schema.dump(contract_detail).data
	if data.get('created_by') != g.user.get('id'):
		return custom_response({'error': 'permission denied'}, 400)

	contract_detail.delete()
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
