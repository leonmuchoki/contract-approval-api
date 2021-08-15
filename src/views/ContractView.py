from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.ContractModel import ContractModel, ContractSchema
from ..models.ContractClauseModel import ContractClauseModel, ContractClauseSchema

contract_api = Blueprint('contract_api', __name__)
contract_schema = ContractSchema()
contract_clause_schema = ContractClauseSchema()


@contract_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
	"""
	Create Contract Function
	"""
	req_data = request.get_json()
	req_data['created_by'] = g.user.get('id')
	#print('req_data')
	#print(req_data)

	#data, error = contract_schema.load(req_data)
	#if error:
	#	return custom_response(error, 400)
	contract = ContractModel(req_data)
	contract.save()
	contract_data = contract_schema.dump(contract)

	#create/initiate contract clause with created contract id
	# clause_data = {}
	# clause_data['created_by'] = g.user.get('id')
	# clause_data['contract_id'] = contract_data.get('id')
	# clause = ContractClauseModel(clause_data)
	# clause.save()

	return custom_response(contract_data, 201)


@contract_api.route('/', methods=['GET'])
def get_all():
	"""
	Get All Contracts
	"""
	contracts = ContractModel.get_all_contracts()
	data = contract_schema.dump(contracts, many=True)
	#print('contracts data::')
	#print(data)
	return custom_response(data, 200)


@contract_api.route('/<int:contract_id>', methods=['GET'])
def get_one(contract_id):
	"""
	Get A Contract 
	"""
	contract = ContractModel.get_one_contract(contract_id)
	if not contract:
		return custom_response({'error': 'contract not found'}, 404)
	data = contract_schema.dump(contract)
	return custom_response(data, 200)


@contract_api.route('/<int:contract_id>', methods=['PUT'])
@Auth.auth_required
def update(contract_id):
    """
    Update A Contract
    """
    req_data = request.get_json()
    req_data['modified_by'] = g.user.get('id')
    
    contract = ContractModel.get_one_contract(contract_id)
    if not contract:
        return custom_response({'error': 'contract not found'}, 404)
    data = contract_schema.dump(contract)

    data, error = contract_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)
    contract.update(data)

    data = contract_schema.dump(contract)
    return custom_response(data, 200)


@contract_api.route('/<int:contract_id>', methods=['DELETE'])
@Auth.auth_required
def delete(contract_id):
	"""
	Delete A Contract
	"""
	contract = ContractModel.get_one_contract(contract_id)
	if not contract:
		return custom_response({'error': 'contract not found'}, 404)
	data = contract_schema.dump(contract)
	
	contract.delete()
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
