import decimal
from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.ProductModel import ProductModelSchema, ProductModel

product_api = Blueprint('product_api', __name__)
product_schema = ProductModelSchema()


@product_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
	"""
	Create Product Function
	"""
	req_data = request.get_json()
	req_data['created_by'] = g.user.get('id')
	data, error = product_schema.load(req_data)
	if error:
		return custom_response(error, 400)
	product = ProductModel(data)
	product.save()
	data = product_schema.dump(product)
	return custom_response(data, 201)


@product_api.route('/', methods=['GET'])
def get_all():
	"""
	Get All Products
	"""
	products = ProductModel.get_all_products()
	data = product_schema.dump(products, many=True)
	return custom_response(data, 200)


@product_api.route('/<int:product_id>', methods=['GET'])
def get_one(product_id):
	"""
	Get A Product
	"""
	product = ProductModel.get_one_product(product_id)
	if not product:
		return custom_response({'error': 'product not found'}, 404)
	data = product_schema.dump(product)
	return custom_response(data, 200)


@product_api.route('/<int:product_id>', methods=['PUT'])
@Auth.auth_required
def update(product_id):
	"""
	Update A Product
	"""
	req_data = request.get_json()
	product = ProductModel.get_one_product(product_id)
	if not product:
		return custom_response({'error': 'product not found'}, 404)
	data = product_schema.dump(product)
	
	data, error = product_schema.load(req_data, partial=True)
	if error:
		return custom_response(error, 400)
	product.update(data)

	data = product_schema.dump(product)
	return custom_response(data, 200)


@product_api.route('/<int:product_id>', methods=['DELETE'])
@Auth.auth_required
def delete(product_id):
	"""
	Delete A Product
	"""
	product = ProductModel.get_one_product(product_id)
	if not product:
		return custom_response({'error': 'product not found'}, 404)
	product.delete()
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

class Encoderr(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)
