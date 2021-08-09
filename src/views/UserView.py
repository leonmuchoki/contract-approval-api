from flask import request, json, Response, Blueprint, g, jsonify, make_response
from ..models.UserModel import UserModel, UserSchema
from ..models.RoleModel import RoleModel, RoleSchema
from ..shared.Authentication import Auth

user_api = Blueprint('user_api', __name__)
user_schema = UserSchema()
role_schema = RoleSchema()


@user_api.route('/register', methods=['POST'])
def create():
	"""
	Create User Function
	"""
	req_data = request.get_json()
	#data, error = user_schema.load(req_data)

	#if error:
	#	return custom_response(req_data, 400)

	# check if user already exist in the db
	user_in_db = UserModel.get_user_by_email(req_data.get('email'))
	if user_in_db:
		message = {'error': 'User already exist, please supply another email address'}
		return custom_response(message, 400)

	user = UserModel(req_data)
	user.save()
	user_data = user_schema.dump(user)
	token = Auth.generate_token(user_data.get('id'))
	return make_response(jsonify({'jwt_token': token}), 200)#custom_response({'jwt_token': token}, 201)


@user_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
	"""
	Get all users
	"""
	users = UserModel.get_all_users()
	ser_users = user_schema.dump(users, many=True)
	return custom_response(ser_users, 200)


@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id):
	"""
	Get a single user
	"""
	user = UserModel.get_one_user(user_id)
	if not user:
		return custom_response({'error': 'user not found'}, 404)

	ser_user = user_schema.dump(user).data
	return custom_response(ser_user, 200)


@user_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
	"""
	Update me
	"""
	req_data = request.get_json()
	data, error = user_schema.load(req_data, partial=True)
	if error:
		return custom_response(error, 400)

	user = UserModel.get_one_user(g.user.get('id'))
	user.update(data)
	ser_user = user_schema.dump(user).data
	return custom_response(ser_user, 200)


@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
	"""
	Delete a user
	"""
	user = UserModel.get_one_user(g.user.get('id'))
	user.delete()
	return custom_response({'message': 'deleted'}, 204)


@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
	"""
	Get me
	"""
	user = UserModel.get_one_user(g.user.get('id'))
	ser_user = user_schema.dump(user).data
	return custom_response(ser_user, 200)


@user_api.route('/login', methods=['POST'])
def login():
	"""
	User Login Function
	"""
	req_data = request.get_json()

	#data, error = user_schema.load(req_data, partial=True)
	#if error:
	#	return custom_response(error, 400)
	if not req_data.get('email') or not req_data.get('password'):
		return make_response(jsonify({'error': 'you need email and password to sign in'}), 400) #custom_response({'error': 'you need email and password to sign in'}, 400)
	user = UserModel.get_user_by_email(req_data.get('email'))
	if not user:
		return make_response(jsonify({'error': 'invalid credentials'}), 400) #custom_response({'error': 'invalid credentials'}, 400)
	if not user.check_hash(req_data.get('password')):
		return make_response(jsonify({'error': 'invalid credentials'}), 400)#custom_response({'error': 'invalid credentials'}, 400)
	#get user role
	roleId = user.role_id
	role = RoleModel.get_one_role(roleId)
	role_data = role_schema.dump(role)
	user_data = user_schema.dump(user)
	user_data['role_name'] = role_data.get('role_name')
	print('user_data...>')
	print(user_data)
	token = Auth.generate_token(user_data.get('id'))
	print('here...')
	print(token)
	#res = jsonify({'jwt_token': token})
	return custom_response({'auth_token': token, 'user_data': user_data}, 200)


def custom_response(res, status_code):
	"""
	Custom Response Function
	"""
	return Response(
		mimetype="application/json",
		response=json.dumps(res),
		status=status_code
	)
