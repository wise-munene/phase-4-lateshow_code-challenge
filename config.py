from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

app= Flask(__name__)
app.secret_key= '7f5fd7a1212935cd38f36c8d699a42aeb2244b6acf7c6a27c4181bce1e2e0bb0'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.json.compact = False

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)  #ensures the db follows the metadata schema
migrate = Migrate(app, db)
db.init_app(app)
api = Api(app) #able to use flask restful resources 