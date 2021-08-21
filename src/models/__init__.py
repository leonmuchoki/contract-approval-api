from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# initialize our db
db = SQLAlchemy()
bcrypt = Bcrypt()

from .UserModel import UserModel, UserSchema
from .ContractClauseModel import ContractClauseModel, ContractClauseSchema
from .ContractDetailModel import ContractDetailModel, ContractDetailSchema
from .ContractTypeModel import ContractTypeModel, ContractTypeSchema
from .ProductModel import ProductModel, ProductModelSchema
from .RoleModel import RoleModel, RoleSchema
from .TenderModel import TenderModel, TenderModelSchema
from .ClauseModel import ClauseModel, ClauseSchema
from .ClauseDetailsModel import ClauseDetailsModel, ClauseDetailsSchema
from .ClauseSubDetailsModel import ClauseSubDetailsModel, ClauseSubDetailsSchema
from .ClausePartModel import ClausePartModel, ClausePartSchema
#from .ContractStageModel import ContractStageModel, ContractStageSchema
