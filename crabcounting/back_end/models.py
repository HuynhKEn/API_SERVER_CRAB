from flask_bcrypt import generate_password_hash, check_password_hash
from back_end import db
import pymongo
from back_end import bcrypt


def hash_password(password):
    return  bcrypt.generate_password_hash(password)
def check_password(password_db,password):
    
    return bcrypt.check_password_hash(password_db, password)

# class DataRecord(db.Document):
#     image = db.StringField(required=True)
#     predict = db.IntField(required=True)

# class History(db.Document):
#     date =  db.DateTimeField(required=True)
#     list = db.ListField(DataRecord)
#     user = db.ReferenceField(Account)
Account = db['Account']
DataRecord = db['DataRecord']
