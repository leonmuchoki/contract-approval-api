## setup (WINDOWS)
pip install pipenv
pipenv install 
pipenv shell

SET FLASK_ENV=development
SET DB_PASSWORD=YOUR_DB_PASSWORD
SET DB_NAME=YOUR_DB_NAME
SET JWT_SECRET_KEY='SIRI-KALI'

## generate random key to use as jwt_secret_key
>>> import os
>>> os.urandom(24)

## db
 $ flask db migrate -m "Initial migration."
 $ flask db upgrade

## useful resources:
https://github.com/madven/flask-postgres
https://dev.to/dev0928/build-restful-apis-using-python-flask-56c7
https://docs.sqlalchemy.org/en/14/orm/join_conditions.html
https://jasonwatmore.com/post/2019/06/22/angular-8-jwt-authentication-example-tutorial