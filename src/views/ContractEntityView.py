from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.ContractEntityModel import ContractEntityModel, ContractEntitySchema

contract_entity_api = Blueprint('contract_entity_api', __name__)
contract_entity_schema = ContractEntitySchema()


@contract_entity_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
	"""
	Create Contract Entity Function
	"""
	req_data = request.get_json()
	req_data['created_by'] = g.user.get('id')
	
	contract_entity = ContractEntityModel(req_data)
	contract_entity.save()
	data = contract_entity_schema.dump(contract_entity)
	return custom_response(data, 201)


@contract_entity_api.route('/', methods=['GET'])
def get_all():
	"""
	Get All Contract Entities
	"""
	print('contract entity....')
	contract_entities = ContractEntityModel.get_all_contract_entities()
	data = contract_entity_schema.dump(contract_entities, many=True)
	print('contract entity data:')
	print(data)
	return custom_response(data, 200)


@contract_entity_api.route('/<int:contract_entity_id>', methods=['GET'])
def get_one(contract_entity_id):
	"""
	Get A Contract Entity
	"""
	contract_entity = ContractEntityModel.get_one_contract_entity(contract_entity_id)
	if not contract_entity:
		return custom_response({'error': 'contract_entity not found'}, 404)
	data = contract_entity_schema.dump(contract_entity)
	return custom_response(data, 200)


@contract_entity_api.route('/<int:contract_entity_id>', methods=['PUT'])
@Auth.auth_required
def update(contract_entity_id):
    """
    Update A Contract Entity
    """
    req_data = request.get_json()
    req_data['modified_by'] = g.user.get('id')

    contract_entity = ContractEntityModel.get_one_contract_entity(contract_entity_id)
    if not contract_entity:
        return custom_response({'error': 'contract_entity not found'}, 404)
    data = contract_entity_schema.dump(contract_entity)

    data, error = contract_entity_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)
    contract_entity.update(data)

    data = contract_entity_schema.dump(contract_entity)
    return custom_response(data, 200)


@contract_entity_api.route('/<int:contract_entity_id>', methods=['DELETE'])
@Auth.auth_required
def delete(contract_entity_id):
	"""
	Delete A Contract Entity
	"""
	contract_entity = ContractEntityModel.get_one_contract_entity(contract_entity_id)
	if not contract_entity:
		return custom_response({'error': 'contract entity not found'}, 404)
	data = contract_entity_schema.dump(contract_entity)
	
	contract_entity.delete()
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
