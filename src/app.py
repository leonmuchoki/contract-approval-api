from flask import Flask
from flask_cors import CORS

from .config import app_config
from .models import db, bcrypt

# import user_api blueprint
from .views.UserView import user_api as user_blueprint
from .views.ContractClauseView import contract_clause_api as contract_clause_blueprint
from .views.ContractClauseDetailsView import contract_clause_details_api as contract_clause_details_blueprint
from .views.ContractDetailView import contract_detail_api as contract_detail_blueprint
from .views.ContractTypeView import contract_type_api as contract_type_blueprint
from .views.ProductView import product_api as product_blueprint
from .views.RoleView import role_api as role_blueprint
from .views.TenderView import tender_api as tender_blueprint
from .views.ContractView import contract_api as contract_blueprint
from .views.ContractProductView import contract_product_api as contract_product_blueprint
from .views.ContractEntityView import contract_entity_api as contract_entity_blueprint
from .views.ClauseView import clause_api as clause_blueprint
from .views.ClauseDetailsView import clause__details_api as clause_details_blueprint

def create_app():
	import os
	env_name = os.getenv('FLASK_ENV')

	# app initiliazation
	app = Flask(__name__)

	config = {
		'ORIGINS': [
		'http://localhost:4200/',  # Angular
		'http://127.0.0.1:4200',  # Angular
		],
	}
	CORS(app, resources={r"/*": {"origins": "*"}})

	app.config.from_object(app_config[env_name])

	# initializing bcrypt and db
	bcrypt.init_app(app)
	db.init_app(app)

	app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
	app.register_blueprint(role_blueprint, url_prefix='/api/v1/roles')
	app.register_blueprint(contract_clause_blueprint, url_prefix='/api/v1/contractclauses')
	app.register_blueprint(contract_clause_details_blueprint, url_prefix='/api/v1/contractclausedetails')
	app.register_blueprint(contract_detail_blueprint, url_prefix='/api/v1/contractdetails')
	app.register_blueprint(contract_type_blueprint, url_prefix='/api/v1/contract/types')
	app.register_blueprint(product_blueprint, url_prefix='/api/v1/products')
	app.register_blueprint(tender_blueprint, url_prefix='/api/v1/tenders')
	app.register_blueprint(contract_blueprint, url_prefix='/api/v1/contracts')
	app.register_blueprint(contract_product_blueprint, url_prefix='/api/v1/contract/products')
	app.register_blueprint(contract_entity_blueprint, url_prefix='/api/v1/contractentites')
	app.register_blueprint(clause_blueprint, url_prefix='/api/v1/clauses')
	app.register_blueprint(clause_details_blueprint, url_prefix='/api/v1/clause/details')

	@app.route('/', methods=['GET'])
	def index():
		"""
		example endpoint
		"""
		return 'Congratulations! Your part 2 endpoint is working'

	return app

