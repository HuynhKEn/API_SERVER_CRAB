from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token, jwt_required ,get_jwt_identity
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import os
UPLOAD_FOLDER = 'uploads'


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = os.urandom(12).hex()   
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = MongoClient("mongodb://htvic17150:gYyaB9jhUXwQsN4W@cluster0-shard-00-00-ntvrq.mongodb.net:27017,cluster0-shard-00-01-ntvrq.mongodb.net:27017,cluster0-shard-00-02-ntvrq.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.CRAB
jwt = JWTManager(app)

from back_end.views import catalog
app.register_blueprint(catalog)