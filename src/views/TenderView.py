from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.TenderModel import TenderModel, TenderModelSchema

tender_api = Blueprint('tender_api', __name__)
tender_schema = TenderModelSchema()


@tender_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
	"""
	Create Tender Function
	"""
	req_data = request.get_json()
	req_data['created_by'] = g.user.get('id')
	req_data['modified_by'] = g.user.get('id')

	print('tender')
	print(req_data)
	
	tender = TenderModel(req_data)
	tender.save()
	data = tender_schema.dump(tender)
	return custom_response(data, 201)


@tender_api.route('/', methods=['GET'])
def get_all():
	"""
	Get All tender
	"""
	tenders = TenderModel.get_all_tenders()
	data = tender_schema.dump(tenders, many=True)
	print('tender')
	print(tenders)
	return custom_response(data, 200)


@tender_api.route('/<int:tender_id>', methods=['GET'])
def get_one(tender_id):
	"""
	Get A Tender Clause
	"""
	tender = TenderModel.get_one_tender(tender_id)
	if not tender:
		return custom_response({'error': 'tender not found'}, 404)
	data = tender_schema.dump(tender)
	return custom_response(data, 200)


@tender_api.route('/<int:tender_id>', methods=['PUT'])
@Auth.auth_required
def update(tender_id):
	"""
	Update A Tender 
	"""
	req_data = request.get_json()
	tender = TenderModel.get_one_tender(tender_id)
	if not tender:
		return custom_response({'error': 'tender not found'}, 404)
	data = tender_schema.dump(tender)

	data, error = tender_schema.load(req_data, partial=True)
	if error:
		return custom_response(error, 400)
	tender.update(data)

	data = tender_schema.dump(tender)
	return custom_response(data, 200)


@tender_api.route('/<int:tender_id>', methods=['DELETE'])
@Auth.auth_required
def delete(tender_id):
	"""
	Delete A  Tender
	"""
	tender = TenderModel.get_one_tender(tender_id)
	if not tender:
		return custom_response({'error': 'tender not found'}, 404)

	tender.delete()
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
