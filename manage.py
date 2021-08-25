import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src.models import RoleModel, ProductModel, ContractEntityModel, ContractStatusModel
from src.app import create_app, db


app = create_app()

migrate = Migrate(app=app, db=db)

manager = Manager(app=app)

manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()

@manager.command
def seed():
    "Add seed data to the database."
    roleProc = RoleModel(role_name = 'procurement')
    roleLegal = RoleModel(role_name = 'legal')
    roleFinance = RoleModel(role_name = 'finance')
    roleCEO = RoleModel(role_name = 'ceo')
    roleSupplier = RoleModel(role_name = 'supplier')
    roleAdmin = RoleModel(role_name = 'admin')

    db.session.add(roleProc)
    db.session.add(roleLegal)
    db.session.add(roleFinance)
    db.session.add(roleCEO)
    db.session.add(roleSupplier)
    db.session.add(roleAdmin)

    initiateContract = ContractStatusModel(status = 'initiated')
    approveContract = ContractStatusModel(status = 'approved')
    rejectContract = ContractStatusModel(status = 'rejected')

    db.session.add(initiateContract)
    db.session.add(approveContract)
    db.session.add(rejectContract)

    kemsaEntity = ContractEntityModel(entity_name='Kenya Medical Supplies Authority')
    umasaEntity = ContractEntityModel(entity_name='Umasa Services and Solutions Ltd')

    db.session.add(kemsaEntity)
    db.session.add(umasaEntity)

    prodData = {'name': 'Desk Calendar', 'price': 360.0}
    prodData2 = {'name': 'Pocket Diary', 'price': 250.0}
    productDesk = ProductModel(prodData)
    productDiary = ProductModel(prodData2)

    db.session.add(productDesk)
    db.session.add(productDiary)

    db.session.commit()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()

if __name__ == '__main__':
  manager.run()
