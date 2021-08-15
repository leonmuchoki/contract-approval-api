from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.ClauseDetailsModel import ClauseDetailsModel, ClauseDetailsSchema

clause__details_api = Blueprint('clause__details_api', __name__)
clause_details_schema = ClauseDetailsSchema()


@clause__details_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
	"""
	Create Clause details Function
	"""
	req_data = request.get_json()
	req_data['created_by'] = g.user.get('id')

	clause_details = ClauseDetailsModel(req_data)
	clause_details.save()
	data = clause_details_schema.dump(req_data)
	return custom_response(data, 201)


@clause__details_api.route('/', methods=['GET'])
def get_all():
	"""
	Get All Clause Details
	"""
	clause_details = ClauseDetailsModel.get_all_clause_details()
	data = clause_details_schema.dump(clause_details, many=True)
	return custom_response(data, 200)


@clause__details_api.route('/<int:clause_details_id>', methods=['GET'])
def get_one(clause_details_id):
	"""
	Get A Clause Details
	"""
	clauseD = ClauseDetailsModel.get_one_clause_detail(clause_details_id)
	if not clauseD:
		return custom_response({'error': 'clause detail not found'}, 404)
	data = clause_details_schema.dump(clauseD)
	return custom_response(data, 200)


@clause__details_api.route('/<int:clause_details_id>', methods=['PUT'])
@Auth.auth_required
def update(clause_details_id):
	"""
	Update A Clause
	"""
	req_data = request.get_json()
	clauseD = ClauseDetailsModel.get_one_clause_detail(clause_details_id)
	if not clauseD:
		return custom_response({'error': ' clause detail not found'}, 404)
	clause = clause_details_schema.dump(clauseD)
	if clauseD.get('created_by') != g.user.get('id'):
		return custom_response({'error': 'permission denied'}, 400)

	data, error = clause_details_schema.load(req_data, partial=True)
	if error:
		return custom_response(error, 400)
	clause.update(data)

	data = clause_details_schema.dump(clause)
	return custom_response(data, 200)


@clause__details_api.route('/<int:clause_details_id>', methods=['DELETE'])
@Auth.auth_required
def delete(clause_details_id):
	"""
	Delete A Clause
	"""
	clause = ClauseDetailsModel.get_one_clause(clause_details_id)
	if not clause:
		return custom_response({'error': ' clause details not found'}, 404)
	data = clause_details_schema.dump(clause)
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
