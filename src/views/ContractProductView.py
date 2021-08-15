from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.ContractProductModel import ContractProductSchema, ContractProductModel

contract_product_api = Blueprint('contract_product_api', __name__)
contract_product_schema = ContractProductSchema()


@contract_product_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
	"""
	Create Contract Product Function
	"""
	req_data = request.get_json()
	req_data['created_by'] = g.user.get('id')
	print('req_data')
	print(req_data)
	contract_prod = ContractProductModel(req_data)
	contract_prod.save()
	data = contract_product_schema.dump(contract_prod)
	return custom_response(data, 201)


@contract_product_api.route('/', methods=['GET'])
def get_all():
	"""
	Get All Contract Entities
	"""
	contract_products = ContractProductModel.get_all_contract_products()
	data = contract_product_schema.dump(contract_products, many=True)
	return custom_response(data, 200)


@contract_product_api.route('/<int:contract_product_id>', methods=['GET'])
def get_one(contract_product_id):
	"""
	Get A Contract Product
	"""
	contract_prod = ContractProductModel.get_one_contract_product(contract_product_id)
	if not contract_prod:
		return custom_response({'error': 'contract_prod not found'}, 404)
	data = contract_product_schema.dump(contract_prod)
	return custom_response(data, 200)


@contract_product_api.route('/<int:contract_product_id>', methods=['PUT'])
@Auth.auth_required
def update(contract_product_id):
    """
    Update A Contract Product
    """
    req_data = request.get_json()
    req_data['modified_by'] = g.user.get('id')

    contract_prod = ContractProductModel.get_one_contract_product(contract_product_id)
    if not contract_prod:
        return custom_response({'error': 'contract_entity not found'}, 404)
    data = contract_product_schema.dump(contract_prod)

    data, error = contract_product_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)
    contract_prod.update(data)

    data = contract_product_schema.dump(contract_prod)
    return custom_response(data, 200)


@contract_product_api.route('/<int:contract_product_id>', methods=['DELETE'])
@Auth.auth_required
def delete(contract_product_id):
	"""
	Delete A Contract Product
	"""
	contract_prod = ContractProductModel.get_one_contract_product(contract_product_id)
	if not contract_prod:
		return custom_response({'error': 'contract contract_prod not found'}, 404)
	data = contract_product_schema.dump(contract_prod)
	
	contract_prod.delete()
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
