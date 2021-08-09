from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.RoleModel import RoleSchema, RoleModel

role_api = Blueprint('role_api', __name__)
role_schema = RoleSchema()


@role_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
	"""
	Create Role Function
	"""
	req_data = request.get_json()
	data, error = role_schema.load(req_data)
	if error:
		return custom_response(error, 400)
	role = RoleModel(data)
	role.save()
	data = role_schema.dump(role).data
	return custom_response(data, 201)


@role_api.route('/', methods=['GET'])
def get_all():
	"""
	Get All Roles
	"""
	roles = RoleModel.get_all_roles()
	data = role_schema.dump(roles, many=True)
	return custom_response(data, 200)


@role_api.route('/<int:role_id>', methods=['GET'])
def get_one(role_id):
	"""
	Get A Role
	"""
	role = RoleModel.get_one_role(role_id)
	if not role:
		return custom_response({'error': 'role not found'}, 404)
	data = role_schema.dump(role)
	return custom_response(data, 200)


@role_api.route('/<int:role_id>', methods=['PUT'])
@Auth.auth_required
def update(role_id):
	"""
	Update A Role
	"""
	req_data = request.get_json()
	role = RoleModel.get_one_role(role_id)
	if not role:
		return custom_response({'error': 'role not found'}, 404)
	data = role_schema.dump(role).data
	
	data, error = role_schema.load(req_data, partial=True)
	if error:
		return custom_response(error, 400)
	role.update(data)

	data = role_schema.dump(role).data
	return custom_response(data, 200)


@role_api.route('/<int:role_id>', methods=['DELETE'])
@Auth.auth_required
def delete(role_id):
	"""
	Delete A Role
	"""
	role = RoleModel.get_one_role(role_id)
	if not role:
		return custom_response({'error': 'role not found'}, 404)
	role.delete()
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
