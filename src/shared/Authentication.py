import jwt
import os
import datetime
from flask import json, Response, request, g
from functools import wraps
from ..models.UserModel import UserModel


class Auth():
	"""
	Auth Class
	"""

	@staticmethod
	def generate_token(user_id):
		"""
		Generate Token Method
		"""
		try:
			payload = {
				'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
				'iat': datetime.datetime.utcnow(),
				'sub': user_id
			}
			return jwt.encode(
				payload,
				os.getenv('JWT_SECRET_KEY'),
				algorithm='HS256'
			)#.decode("utf-8")
		except Exception as e:
			return Response(
				mimetype="application/json",
				response=json.dumps({'error': e}),
				status=400
			)

	@staticmethod
	def decode_token(token):
		"""
		Decode token method
		"""
		re = {'data': {}, 'error': {}}
		try:
			# print('payload')
			# print(token)
			# print('JWT_SECRET_KEY')
			# print(os.getenv('JWT_SECRET_KEY'))
			payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=["HS256"])
			#print('payload')
			#print(payload)
			re['data'] = {'user_id': payload['sub']}
			return re
		except jwt.ExpiredSignatureError as e1:
			re['error'] = {'message': 'token expired, please login again'}
			return re
		except jwt.InvalidTokenError:
			re['error'] = {'message': 'Invalid token, please try again with a new token'}
			return re

	# decorator
	@staticmethod
	def auth_required(func):
		"""
		Auth decorator
		"""

		@wraps(func)
		def decorated_auth(*args, **kwargs):
			#if 'auth_token' not in request.headers:
			if 'Authorization' not in request.headers:
				return Response(
					mimetype="application/json",
					response=json.dumps({'error': 'Authentication token is not available, please login to get one'}),
					status=400
				)
			token = request.headers.get('api-token')
			auth_header = request.headers.get('Authorization')
			if auth_header:
				token = auth_header.split(" ")[1]
			else:
				token = ''

			# print('token')
			# print(token)

			data = Auth.decode_token(token)
			if data['error']:
				return Response(
					mimetype="application/json",
					response=json.dumps(data['error']),
					status=400
				)

			user_id = data['data']['user_id']
			check_user = UserModel.get_one_user(user_id)
			if not check_user:
				return Response(
					mimetype="application/json",
					response=json.dumps({'error': 'user does not exist, invalid token'}),
					status=400
				)
			g.user = {'id': user_id}
			return func(*args, **kwargs)

		return decorated_auth
