from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.ContractTypeModel import ContractTypeModel, ContractTypeSchema

contract_type_api = Blueprint('contract_type_api', __name__)
contract_type_schema = ContractTypeSchema()


@contract_type_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
	"""
	Create Contract Type Function
	"""
	req_data = request.get_json()

	contract_type = ContractTypeModel(req_data)
	contract_type.save()
	data = contract_type_schema.dump(contract_type)
	return custom_response(data, 201)


@contract_type_api.route('/', methods=['GET'])
def get_all():
	"""
	Get All Contract Types
	"""
	contract_types = ContractTypeModel.get_all_contract_types()
	data = contract_type_schema.dump(contract_types, many=True)
	return custom_response(data, 200)


@contract_type_api.route('/<int:contract_type_id>', methods=['GET'])
def get_one(contract_type_id):
	"""
	Get A Contract type
	"""
	post = ContractTypeModel.get_one_contract_type(contract_type_id)
	if not post:
		return custom_response({'error': 'contract type not found'}, 404)
	data = contract_type_schema.dump(post).data
	return custom_response(data, 200)


@contract_type_api.route('/<int:contract_type_id>', methods=['PUT'])
@Auth.auth_required
def update(contract_type_id):
	"""
	Update A Contract Type
	"""
	req_data = request.get_json()
	contract_type = ContractTypeModel.get_one_contract_type(contract_type_id)
	if not contract_type:
		return custom_response({'error': 'contract_type not found'}, 404)
	data = contract_type_schema.dump(contract_type).data
	
	data, error = contract_type_schema.load(req_data, partial=True)
	if error:
		return custom_response(error, 400)
	contract_type.update(data)

	data = contract_type_schema.dump(contract_type)
	return custom_response(data, 200)


@contract_type_api.route('/<int:contract_type_id>', methods=['DELETE'])
@Auth.auth_required
def delete(contract_type_id):
	"""
	Delete A Contract Type
	"""
	contract_type = ContractTypeModel.get_one_contract_type(contract_type_id)
	if not contract_type:
		return custom_response({'error': 'contract type not found'}, 404)
	data = contract_type_schema.dump(contract_type)
	
	contract_type.delete()
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
